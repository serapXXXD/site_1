from rest_framework import routers
from django.urls import path
from .views import CategoryViewSet, UserViewSet, PostViewSet, GetTokenAPIView, TagViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register('cats', CategoryViewSet)
router.register('users', UserViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('login/', GetTokenAPIView.as_view(), name='login'),
              ] + router.urls
