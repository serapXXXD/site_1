from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth.views import LogoutView 

app_name = 'authentication'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
]

