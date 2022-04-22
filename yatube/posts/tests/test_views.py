from pprint import pprint

from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()

USERNAME = 'Test_user'
GROUP_POST_SLAG = 'test_slug'

INDEX = reverse('posts:index')
GROUP_POST = reverse('posts:group_posts',
                     kwargs={'slug': GROUP_POST_SLAG}
                     )
PROFILE = reverse('posts:profile',
                  kwargs={'username': USERNAME}
                  )
CREATE_POST = reverse('posts:post_create')
AUTH = reverse('users:login')


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug=GROUP_POST_SLAG
        )
        cls.post = Post.objects.create(
            text='Тестовый пост 1',
            author=cls.user,
            group=cls.group
        )
        cls.DETAIL_POST = reverse('posts:post_detail',
                                  kwargs={'post_id': cls.post.pk}
                                  )
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post.pk}
                                )
        cls.guest_client = Client()

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def setUp(self) -> None:
        pass

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_page_names = {
            INDEX: 'posts/index.html',
            GROUP_POST: 'posts/group_list.html',
            PROFILE: 'posts/profile.html',
            self.DETAIL_POST: 'posts/post_detail.html',
            CREATE_POST: 'posts/create_post.html',
            self.POST_EDIT: 'posts/create_post.html'
        }
        for url, template in templates_page_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_index_and_group_posts_and_profile_correct_context(self):
        """
        Шаблоны posts:index, posts:group_posts и posts:profile
        сформирован с правильным контекстом.
        """

        urls = [
            INDEX,
            GROUP_POST,
            PROFILE,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                first_object = response.context['page_obj'][0]
                if url == GROUP_POST:
                    self.assertEqual(first_object.text, 'Тестовый пост 1')
                    self.assertEqual(first_object.author.username, USERNAME)
                    self.assertEqual(first_object.group.slug, GROUP_POST_SLAG)
                self.assertEqual(first_object.text, 'Тестовый пост 1')
                self.assertEqual(first_object.author.username, USERNAME)

    def test_post_detail_correct_context(self):
        """Шаблон posts:post_detail сформированы с правильным контекстом."""

        response = self.guest_client.get(self.DETAIL_POST)
        detail_post = response.context['detail_post']
        self.assertEqual(detail_post.text, 'Тестовый пост 1')
        self.assertEqual(detail_post.author.username, USERNAME)

    def test_post_create_correct_context(self):
        """
        Шаблон posts:post_create и posts:post_edit
        сформированы с правильным контекстом.
        """

        urls = [CREATE_POST, self.POST_EDIT]

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                for url in urls:
                    client = self.authorized_client.get(url)
                    form_field = client.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.post = Post.objects.bulk_create(
            [Post(
                text=f'test_post_text_{i}',
                author=cls.user
            ) for i in range(1, 14)]
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
            slug=GROUP_POST_SLAG
        )

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_page_contains_ten_records(self):
        """Определяет правильность вывода постов на странице."""
        COUNT_POSTS_ONE_PAGE = 10
        a = [INDEX, GROUP_POST, PROFILE]
        for url in a:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.context['object_list'], 10)
        # response_one_page = self.guest_client.get(INDEX)
        # response_second_page = self.guest_client(INDEX + '?page=2')
        # self.assertEqual(len(response_one_page.context['object_list']), 10)
        # self.assertEqual(len(response_second_page.context['object_list']), 3)
