from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Tag, Comment
from django.db.models import Q
from django.views.generic import ListView
from .forms import PostForm, CommentForm
from authentication.models import Subscription


class IndexSearchView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    # ?tags=tag_1&tags=tag_2&tags=tag_3

    def get_queryset(self):
        queryset = super().get_queryset()
        query, query_tags = self.get_filters()
        # найти метод который исключает символы

        if query and query not in '@#$%^&*()_+=':
            queryset = queryset.filter(
                Q(body__icontains=query) | Q(title__icontains=query))
            print(query)

        if query_tags:
            tags = Tag.objects.filter(slug__in=query_tags)
            queryset = queryset.filter(tags__in=tags)
        return queryset

    def get_filters(self):
        query_tags = self.request.GET.getlist('tags', '')
        query = self.request.GET.get('search')
        return query, query_tags

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query, query_tags = self.get_filters()
        context['tags'] = Tag.objects.all()
        context['query'] = query
        context['query_tags'] = query_tags
        return context




def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_title = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post', post_id)
    is_subscribe = False

    if request.user.is_authenticated:
        is_subscribe = Subscription.objects.filter(subscriber=request.user, author=post.author).exists()

    context = {
        'is_subscribe': is_subscribe,
        'post': post,
        'post_title': post_title,
        'form': form,
    }
    print(request.user)
    return render(request, 'blog/post.html', context)


def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    print('request form', request.POST)

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        tags = form.cleaned_data.pop('tags')
        new_post.tags.add(*tags)
        return redirect('blog:index')
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


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return render(request, 'blog/delete_post_comment.html')


def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author or request.user == comment.author:
        comment.delete()
    return render(request, 'blog/delete_post_comment.html')
