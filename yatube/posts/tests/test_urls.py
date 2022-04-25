from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .utils_tests import TestVariables as data
from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug=data.GROUP_POST_SLAG.value,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post.pk}
                                )
        cls.DETAIL_POST = reverse('posts:post_detail',
                                  kwargs={'post_id': cls.post.pk}

                                  )

    def setUp(self):
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_codes(self):
        """Страницы доступны любому пользователю."""

        CODE_SUCCESS = 200
        CODE_REDIRECT = 302
        CODE_NOT_FOUND = 404

        url_names = [
            [self.authorized_client, data.CREATE_POST.value, CODE_SUCCESS],
            [self.authorized_client, self.POST_EDIT, CODE_SUCCESS],
            [self.authorized_client, self.DETAIL_POST, CODE_SUCCESS],
            [self.authorized_client, data.FAKE_PAGE.value, CODE_NOT_FOUND],
            [self.guest_client, data.INDEX.value, CODE_SUCCESS],
            [self.guest_client, data.CREATE_POST.value, CODE_REDIRECT],
            [self.guest_client, self.POST_EDIT, CODE_REDIRECT],
            [self.guest_client, data.GROUP_POST.value, CODE_SUCCESS],
            [self.guest_client, data.PROFILE.value, CODE_SUCCESS],
            [self.guest_client, self.DETAIL_POST, CODE_SUCCESS],
            [self.guest_client, data.FAKE_PAGE.value, CODE_NOT_FOUND]
        ]
        for client, url, code in url_names:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(
                    code,
                    response.status_code
                )

    def test_redirect(self):
        """Перенаправление пользователя."""

        templates_url_names = [
            [
                self.guest_client,
                data.CREATE_POST.value,
                data.AUTH.value + '?next=' + data.CREATE_POST.value
            ],
            [
                self.guest_client,
                self.POST_EDIT,
                data.AUTH.value + '?next=' + self.POST_EDIT
            ],
        ]
        for client, url, url_redirect in templates_url_names:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertRedirects(
                    response,
                    url_redirect
                )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            data.INDEX.value: 'posts/index.html',
            data.GROUP_POST.value: 'posts/group_list.html',
            self.DETAIL_POST: 'posts/post_detail.html',
            data.PROFILE.value: 'posts/profile.html',
            data.CREATE_POST.value: 'posts/create_post.html',
            self.POST_EDIT: 'posts/create_post.html'
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
