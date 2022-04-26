from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()

USERNAME = 'Test_User'
LOGOUT = reverse('users:logout')
SIGNUP = reverse('users:signup')
LOGIN = reverse('users:login')
PASSWORD_CHANGE = reverse('users:password_change')
PASSWORD_CHANGE_DONE = reverse('users:password_change_done')
PASSWORD_RESET = reverse('users:password_reset')
PASSWORD_RESET_DONE = reverse('users:password_reset_done')
# PASSWORD_RESET_CONFIRM = reverse('users:password_reset_confirm')
PASSWORD_RESET_COMPETE = reverse('users:password_reset_compete')


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)

    def setUp(self) -> None:
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_auth_users_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_pages_names = [
            [LOGOUT, 'users/logged_out.html'],
            [SIGNUP, 'users/signup.html'],
            [LOGIN, 'users/login.html'],
            [PASSWORD_CHANGE, 'users/password_change.html'],
            [PASSWORD_CHANGE_DONE, 'users/password_change_done.html'],
            [PASSWORD_RESET, 'users/password_reset.html'],
            [PASSWORD_RESET_DONE, 'users/password_reset_done.html'],
            # [self.guest_client, PASSWORD_RESET_CONFIRM, 'users/password_reset_confirm.html'],
            # [PASSWORD_RESET_COMPETE, 'users/password_reset_compete.html']
        ]
        for url, template in templates_pages_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                print(response)
                self.assertTemplateUsed(response, template)

    def test_signup_correct_context(self):
        """Шаблон users:signup сфомирован с правильным контекстом."""

        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                client = self.guest_client.get(SIGNUP)
                form_field = client.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
