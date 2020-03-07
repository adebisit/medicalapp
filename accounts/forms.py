from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class SignupForm(UserCreationForm):
    group = forms.CharField(max_length=200)
    email = forms.EmailField(label="Email", max_length=200, help_text="Required")
    first_name = forms.CharField(label="Name", max_length=200, help_text="Required")
    last_name = forms.CharField(label="Company Name", max_length=200, help_text="Required")


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')