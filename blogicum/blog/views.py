from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .constants import POSTS_ON_MAIN_PAGE
from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.annotate(
        comment_count=Count('comments')
    ).filtered_posts('category').order_by('-pub_date')
    paginator = Paginator(post_list, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post = get_object_or_404(
            Post.objects.select_related('category', 'location'), pk=post_id
        )
    else:
        post = get_object_or_404(
            Post.objects.filtered_posts('category', 'location'), pk=post_id
        )
    context = {'post': post}
    context['form'] = CommentForm()
    context['comments'] = (
        post.comments.select_related('author')
    )
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    post_list = category.posts.filtered_posts()
    paginator = Paginator(post_list, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}

    return render(
        request,
        'blog/category.html',
        context
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    if request.user.id == profile.id:
        posts = Post.objects.filter(author=profile.id).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
    else:
        posts = Post.objects.filter(author=profile.id).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date').filtered_posts()
    paginator = Paginator(posts, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None, request.FILES or None, instance=instance
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:index')
    return render(request, 'blog/user.html', {'form': form})


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id, author=request.user)
    form = PostForm(instance=instance)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user)
    form = CommentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request, 'blog/comment.html', {'form': form, 'comment': instance}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {})
