from django.urls import path
from rest_framework import routers
from .views import PostListAPIView, PostCreateAPIView, GetTokenAPIView, PatchPostAPIView, DeletePostAPIView, \
    CategoryViewSet, UserViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register('cats', CategoryViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post_list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post_create'),
    path('login/', GetTokenAPIView.as_view(), name='login'),
    path('posts/<int:pk>/update/', PatchPostAPIView.as_view(), name='post_patch'),
    path('posts/<int:pk>/delete/', DeletePostAPIView.as_view(), name='post_delete'),
] + router.urls
