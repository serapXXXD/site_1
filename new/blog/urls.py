from django.urls import path
from .views import (IndexSearchView, show_post, add_post, post_edit,
                    post_delete, comment_edit, comment_delete)

app_name = 'blog'

urlpatterns = [
    path('', IndexSearchView.as_view(), name='index'),
    path('blog/post/<int:post_id>/', show_post, name='post'),
    path('blog/post/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('blog/post/<int:post_id>/delete/', post_delete, name='post_delete'),
    path('blog/add_post/', add_post, name='add_post'),
    path('blog/post/<int:post_id>/comments/<int:comment_id>/edit/',
         comment_edit, name='comment_edit'),
    path('blog/post/<int:post_id>/comments/<int:comment_id>/delete/',
         comment_delete, name='comment_delete'),
]
