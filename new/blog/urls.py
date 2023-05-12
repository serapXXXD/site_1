from django.urls import path
from .views import IndexSearchView, tag_view, show_post, add_post

app_name = 'blog'

urlpatterns = [
    path('', IndexSearchView.as_view(), name='index'),
    path('blog/tag/<slug:tag_slug>/', tag_view, name='tag'),
    path('blog/post/<int:post_id>', show_post, name='post'),
    path('blog/add_post/', add_post, name='add_post'),
]
