from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Ім’я', max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введіть ваше ім’я'}))
    last_name = forms.CharField(label='Прізвище', max_length=30,
                                widget=forms.TextInput(attrs={'placeholder': 'Введіть ваше прізвище'}))
    username = forms.CharField(label='Нік користувача', max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': 'Введіть бажаний нік'}))
    email = forms.EmailField(label='Електронна пошта',
                             widget=forms.EmailInput(attrs={'placeholder': 'Введіть вашу електронну пошту'}))
    phone_number = forms.CharField(label='Номер телефону', max_length=15,
                                   widget=forms.TextInput(attrs={'placeholder': 'Введіть номер телефону'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введіть пароль'}))
    password2 = forms.CharField(label='Підтвердження паролю',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Підтвердіть пароль'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']
        labels = {
            'username': 'Нік користувача',
            'password1': 'Пароль',
            'password2': 'Підтвердження паролю',
        }
        help_texts = {
            'username': 'Це ім’я користувача вже зайняте. Будь ласка, виберіть інше.',
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
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()

        return user
