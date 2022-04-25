import enum

from django.urls import reverse


class TestVariables(enum.Enum):
    USERNAME = 'Test_User'
    GROUP_POST_SLAG = 'test-slug'
    INDEX = reverse('posts:index')
    GROUP_POST = reverse('posts:group_posts',
                         kwargs={'slug': GROUP_POST_SLAG}
                         )
    PROFILE = reverse('posts:profile',
                      kwargs={'username': USERNAME}
                      )
    CREATE_POST = reverse('posts:post_create')
    AUTH = reverse('users:login')
    SIGNUP = reverse('users:signup')
    FAKE_PAGE = '/fake_page/'