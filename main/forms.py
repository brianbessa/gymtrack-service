from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome',
            'class': 'custom-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha',
            'class': 'custom-input'
        })
    )

class CadastroForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-input', 'placeholder': 'Email'}))
    peso = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Peso', 'class': 'custom-input'}))
    altura = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Altura', 'class': 'custom-input'}))
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-input'}))
    experiencia = forms.ChoiceField(required=False, choices=[
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ], widget=forms.Select(attrs={'class': 'custom-input'}))
    objetivo = forms.ChoiceField(required=False, choices=[
        ('Hipertrofia', 'Hipertrofia'),
        ('Emagrecimento', 'Emagrecimento'),
        ('Condicionamento', 'Condicionamento'),
    ], widget=forms.Select(attrs={'class': 'custom-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'peso', 'altura', 'data_nascimento', 'experiencia', 'objetivo']
