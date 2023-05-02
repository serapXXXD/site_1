
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
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


def tag_view(request, tag_id):
    object_list = Post.objects.filter(tags=tag_id)
    tags = Tag.objects.all()
    context = {'tags': tags,
               'object_list': object_list,}
    return render(request, 'tag.html', context)
