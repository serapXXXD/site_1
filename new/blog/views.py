from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Tag, Comment
from allauth.socialaccount.models import SocialAccount
from django.db.models import Q
from django.views.generic import ListView
from .forms import PostForm, CommentForm
from authentication.models import Subscription, Like
import re


class IndexSearchView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query, query_tags, query_user = self.get_filters()

        if query:
            queryset = queryset.filter(
                Q(body__icontains=query) | Q(title__icontains=query) | Q(author__username__icontains=query))

        if query_tags:
            tags = Tag.objects.filter(slug__in=query_tags)
            queryset = queryset.filter(tags__in=tags)

        if query_user:
            queryset = queryset.filter(author__username=query_user)

        return queryset.select_related('author').prefetch_related('likes', 'comments', 'author__socialaccount_set')

    def get_filters(self):
        query_tags = self.request.GET.getlist('tags', '')
        query = self.request.GET.get('search', '')
        query_user = self.request.GET.get('user', '')
        return query, query_tags, query_user

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query, query_tags, query_user = self.get_filters()
        context['social_users'] = [account.user for account in SocialAccount.objects.all().select_related('user')]
        context['tags'] = Tag.objects.all()
        context['query'] = query
        context['query_tags'] = query_tags
        context['query_user'] = query_user

        if 'tags' in str(self.request) or 'user' in str(self.request) or 'search' in str(self.request):
            query_params = str(self.request).split('\'')[1][2:]
            if re.search(r'page=[\d]{0,9}&+', query_params):
                query_params = re.split(r"page=[\d]{1,9}&", query_params)[1]
            context['query_params'] = query_params

        return context


def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_title = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    comments = (Comment.objects.filter(post=post).select_related(
        'author', 'reply_to', 'reply_to__author').prefetch_related('replies', 'author__socialaccount_set'))
    social_users = [acc.user for acc in SocialAccount.objects.all().select_related('user')]

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post', post_id)
    is_subscribe = False

    if request.user.is_authenticated:
        is_subscribe = Subscription.objects.filter(subscriber=request.user, author=post.author).exists()

    like = None
    if request.user.is_authenticated:
        like = Like.objects.filter(liked_post=post, liker=request.user).exists()

    like_list = Like.objects.filter(liked_post=post_id).prefetch_related('liker__socialaccount_set').select_related(
        'liker')
    context = {
        'is_subscribe': is_subscribe,
        'social_users': social_users,
        'post': post,
        'like': like,
        'comments': comments,
        'post_title': post_title,
        'form': form,
        'like_list': like_list,
    }
    return render(request, 'blog/post.html', context)


def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        tags = form.cleaned_data.pop('tags')
        new_post.tags.add(*tags)
        return redirect('blog:index')
    else:
        print(form.errors)
    context = {'form': form}

    return render(request, 'blog/add_post.html', context)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:
        form = PostForm(request.POST or None,
                        request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post', post_id)

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'blog/add_post.html', context)


def comment_edit(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)

    if request.user == comment.author:
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            comment.text = request.POST['text']
            comment.save()
            return redirect('blog:post', post_id)
    context = {
        'comment': comment,
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post.html', context)


def comment_reply(request, comment_id, post_id):
    reply_to = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related(
        'author', 'reply_to', 'reply_to__author').prefetch_related('replies', 'author__socialaccount_set')

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.reply_to = reply_to
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post', post_id)

    context = {
        'reply_to': reply_to,
        'comments': comments,
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post.html', context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.photo.delete()
        post.delete()
    return render(request, 'blog/delete_post_comment.html')


def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author or request.user == comment.author:
        comment.delete()
    return render(request, 'blog/delete_post_comment.html')
