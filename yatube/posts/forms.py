from django import forms

from .models import Group, Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea,
                           label='Текст поста',
                           help_text='Текст нового поста',
                           required=True
                           )
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   label='Группа',
                                   help_text='''
                                        Группа к которой
                                        будет относиться пост
                                   ''',
                                   required=False
                                   )

    class Meta:
        model = Post
        fields = ['text', 'group']
