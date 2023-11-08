from django import forms
import app.models as models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model() 

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('cpf','first_name', 'last_name', 'email')
        labels = {
            'cpf': 'CPF',
            'first_name': 'Nome',
            'last_name': 'Sobrenome'
        }


class LoginForm(forms.Form):
    email = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

