from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .utils_tests import TestVariables as data
from ..models import Post

User = get_user_model()


class FormsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username=data.USERNAME.value)
        cls.post = Post.objects.create(
            text='test_post_1',
            author=cls.user
        )
        cls.POST_EDIT = reverse('posts:post_edit',
                                kwargs={'post_id': cls.post.pk}
                                )
        cls.POST_DETAIL = reverse('posts:post_detail',
                                  kwargs={'post_id': cls.post.pk}
                                  )

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_record_post(self):
        """Проверка создание нового поста."""

        posts_count = Post.objects.count()
        form_data = {
            'text': 'new_post',
            'author': self.user
        }
        response = self.authorized_client.post(
            data.CREATE_POST.value,
            form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, data.PROFILE.value)

    def test_change_record_posts(self):
        """Проверка на изменение записи поста в базе даннхы."""
        form_data = {
            'text': 'modified_post',
        }
        response = self.authorized_client.post(
            self.POST_EDIT,
            form_data,
            follow=True
        )
        self.assertEqual(Post.objects.first().text, 'modified_post')
        self.assertRedirects(response, self.POST_DETAIL)

    def test_check_create_new_user(self):
        """Проверка создания нового пользователя."""
        NAME_USER = 'New_User'
        form_data = {
            # 'first_name': NAME_USER,
            # 'last_name': NAME_USER,
            'username': NAME_USER,
            # 'email': NAME_USER + '@mail.com',
            # 'password1': NAME_USER + '__001',
            # 'password2': NAME_USER + '__001'
        }
        response = self.guest_client.post(
            data.SIGNUP.value,
            form_data,
            follow=True
        )


