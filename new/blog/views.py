from .models import *
from django.db.models import Q

from django.views.generic import TemplateView, ListView


class IndexView(TemplateView):
    template_name = 'index.html'


class ResultSearchIndexView(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query != None:
            object_list = Post.objects.filter(
                Q(body__icontains=query) | Q(title__icontains=query))
        else:
            object_list = Post.objects.all()
        return object_list
