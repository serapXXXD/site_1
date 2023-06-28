from rest_framework import permissions
from blog.models import Post


class IsAuthorOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj_post):
        post = Post.objects.get(id=obj_post.id)
        return request.user == post.author
