from django.urls import path

from .views import (index,
                    group_posts,
                    profile,
                    post_detail,
                    post_create,
                    post_edit
                    )

app_name = 'posts'
urlpatterns = [
    path('group/<slug:slug>/', group_posts, name='group_posts'),
    path('profile/<str:username>/', profile, name='profile'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('create/', post_create, name='post_create'),
    path('', index, name='index'),
]
