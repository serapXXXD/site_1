from django.urls import path
from .views import PostListAPIView, PostCreateAPIView, GetTokenAPIView

app_name = 'api'

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post_list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post_create'),
    path('login/', GetTokenAPIView.as_view(), name='login')
]
