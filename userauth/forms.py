from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Firstname"}))
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Lastname"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"Placeholder": "Email"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'firstname',
            'lastname',
            'email'
        ]