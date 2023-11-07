from django_filters import rest_framework as filters
from blog.models import Post


class PostFilter(filters.FilterSet):
    author__username = filters.CharFilter(lookup_expr='icontains')
    tags__title = filters.CharFilter(lookup_expr='icontains')
    category__title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['author__username', 'tags__title']
