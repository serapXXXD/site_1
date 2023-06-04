from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from .forms import RegisterUserForm, ProfileUserForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('authentication:login')

class ProfileView(UpdateView):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('authentication:profile')
    form_class = ProfileUserForm

    def get_object(self):
        return self.request.user