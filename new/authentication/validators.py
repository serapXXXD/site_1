from django.core.exceptions import ValidationError
from datetime import datetime


class ProfileUserFormValodator:
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) > 20:
            raise ValidationError(
                'Длина имени не должна привышать 20 символов')
        return first_name

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError('Пароли не совпадают')
