from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'username'
    }))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Иван'
    }))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Иванов'
    }))
    email = forms.CharField(label="E-mail", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'user@mail.ru'
    }))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Аккаунт с этим e-mail уже существует!")
