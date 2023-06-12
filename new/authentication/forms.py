from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.password_validation import validate_password
from .validators import ProfileUserFormValodator


User = get_user_model()


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileUserForm(ProfileUserFormValodator, forms.ModelForm, ):
    password1 = forms.CharField(
        widget=forms.PasswordInput, required=False, validators=[validate_password])
    password2 = forms.CharField(
        widget=forms.PasswordInput, required=False, )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
