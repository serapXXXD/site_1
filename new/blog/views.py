
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q

from django.views.generic import ListView


class IndexSearchView(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('search')

        if query and query != '@#$%^&*()_+=':
            object_list = Post.objects.filter(
                Q(body__icontains=query) | Q(title__icontains=query))
        else:
            object_list = Post.objects.all()
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['tags'] = Tag.objects.all()
        return context


def tag_view(request, tag_slug):
    object_list = Post.objects.filter(tags__slug=tag_slug)
    tags = Tag.objects.all()
    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tag_title = get_object_or_404(Tag, slug=tag_slug)
    context = {'tags': tags,
               'tag_title': tag_title,
               'page_obj': page_obj, }
    return render(request, 'tag.html', context)
