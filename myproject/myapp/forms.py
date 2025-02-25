from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Document

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="Имя пользователя",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем русские сообщения об ошибках
        self.fields['username'].error_messages = {
            'required': 'Пожалуйста, введите имя пользователя.',
            'unique': 'Пользователь с таким именем уже существует.',
        }
        self.fields['password1'].error_messages = {
            'required': 'Пожалуйста, введите пароль.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Пожалуйста, подтвердите пароль.',
            'password_mismatch': 'Пароли не совпадают.',
        }
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Имя пользователя',
            'password': 'Пароль',
        }
        error_messages = {
            'username': {
                'required': 'Пожалуйста, введите имя пользователя.',
            },
            'password': {
                'required': 'Пожалуйста, введите пароль.',
            },
            'invalid_login': 'Неверное имя пользователя или пароль.',
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['zip_file']
        labels = {
            'zip_file': 'Загрузите ZIP-файл',
        }
        error_messages = {
            'zip_file': {
                'required': 'Пожалуйста, выберите файл для загрузки.',
            },
        }