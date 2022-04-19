from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Класс определяет модель постов."""

    text = models.TextField(verbose_name='Текст',
                            help_text='Введите текст поста'
                            )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации'
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_info',
                               verbose_name='Автор'
                               )
    group = models.ForeignKey('Group',
                              on_delete=models.SET_NULL,
                              related_name='group_info',
                              verbose_name='Группа',
                              help_text='Группа, к которой будет относиться пост',
                              blank=True,
                              null=True
                              )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    """Класс определяет модель групп к постам."""

    title = models.CharField(max_length=200,
                             verbose_name='Название'
                             )
    slug = models.SlugField(max_length=200,
                            unique=True
                            )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
