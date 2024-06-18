from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cart


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Ім’я', max_length=30)
    last_name = forms.CharField(label='Прізвище', max_length=30)
    username = forms.CharField(label="Нік користувача", max_length=30)
    phone_number = forms.CharField(label='Номер телефону', max_length=15)
    email = forms.EmailField(label='Електронна пошта')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Ім’я користувача',
            'password1': 'Пароль',
            'password2': 'Підтвердження паролю',
        }
        help_texts = {
            'password1': 'Ваш пароль повинен містити щонайменше 8 символів.',
        }
        error_messages = {
            'username': {
                'unique': 'Це ім’я користувача вже зайняте. Будь ласка, виберіть інше.',
            },
        }

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

