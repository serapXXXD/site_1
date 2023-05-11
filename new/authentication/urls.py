from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegiterUser.as_view(), name='register'),
]
