from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date

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
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Informe seu usuário'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-input', 'placeholder': 'Informe seu email'}))
    peso = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Peso', 'class': 'custom-input'}))
    altura = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Altura', 'class': 'custom-input'}))
    data_nascimento = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-input'}))
    experiencia = forms.ChoiceField(required=True, choices=[
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ], widget=forms.Select(attrs={'class': 'custom-input'}))
    objetivo = forms.ChoiceField(required=True, choices=[
        ('Hipertrofia', 'Hipertrofia'),
        ('Emagrecimento', 'Emagrecimento'),
        ('Condicionamento', 'Condicionamento'),
    ], widget=forms.Select(attrs={'class': 'custom-input'}))

    error_messages = {
        'password_mismatch': 'As senhas não coincidem. Verifique novamente.',
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'peso', 'altura', 'data_nascimento', 'experiencia', 'objetivo']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Esse nome de usuário já existe. Experimente outro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse email já existe. Experimente outro.")
        return email
    
    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')

        if data_nascimento:
            hoje = date.today()

            if data_nascimento > hoje:
                raise forms.ValidationError("A data de nascimento não pode ser no futuro.")

            idade = hoje.year - data_nascimento.year - (
                (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
            )

            if idade > 120:
                raise forms.ValidationError("Idade inválida. Por favor, insira uma data realista.")

            if idade < 18:
                raise forms.ValidationError("Você precisa ter pelo menos 18 anos para se cadastrar.")

        return data_nascimento