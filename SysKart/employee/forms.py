from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import EmployeeDetails


class SignUpForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ["username", "name", "address", "email", "phone_number", "password"]


class LoginForm(forms.Form):
    """Create a new user and stuff."""

    username = forms.CharField(max_length=140)
    password = forms.CharField(max_length=140, widget=forms.PasswordInput(), required=True)
