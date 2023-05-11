from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from django.urls import reverse_lazy


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('authentication:login')