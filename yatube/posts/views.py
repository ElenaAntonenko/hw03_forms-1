from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User
from .utils import install_paginator


def index(request):
    post_list = Post.objects.select_related('group', 'author').all()
    context = {
        'page_obj': install_paginator(request, post_list),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_info.select_related('author').all()
    context = {
        'group': group,
        'page_obj': install_paginator(request, posts),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('group',
                                        'author').filter(author_id=author.pk)
    context = {
        'page_obj': install_paginator(request, posts),
        'author': author
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    detail_post = Post.objects.select_related('author',
                                              'group').get(pk=post.pk)
    count_posts = Post.objects.filter(author_id=detail_post.author.pk).count()
    context = {
        'detail_post': detail_post,
        'count_posts_author': count_posts
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.author_id = request.user.pk
            save_form.save()
            return redirect('posts:profile', username=request.user.username)

    form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.author_id = request.user.pk
            save_form.pk = post_id
            save_form.save()
            return redirect('posts:post_detail', post_id)
    else:
        form = PostForm(instance=post)
        context = {'form': form,
                   'is_edit': True,
                   'post_id': post_id
                   }
        return render(request, 'posts/create_post.html', context)
