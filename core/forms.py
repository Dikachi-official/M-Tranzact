from django import forms
from userauth.models import User
from account.models import Account, Kyc
from django.shortcuts import render, redirect


# TO REGISTER KYC
class KycRegistrationForm(forms.ModelForm):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female")
    )

    MARITAL_CHOICES = (
        ("single", "Single"),
        ("marrried", "Married")
    )

    IDENTITY_CHOICES = (
        ("national id card", "National ID Card"),
        ("drivers licence", "Drivers Licence"),
        ("international passport", "International Passport")
    )

    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Fullname"}))
    marital_status = forms.ChoiceField(choices=MARITAL_CHOICES, widget=forms.Select(attrs={"class":"form-control", "placeholder": "marital status"}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={"class":"form-control", "placeholder": "gender"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "State"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "city"}))
    country = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "country"}))
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "mobile"}))
    image = forms.ImageField(label="Profile Picture", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    id_select = forms.ChoiceField(choices=IDENTITY_CHOICES, widget=forms.Select(attrs={"class":"form-control", "placeholder": "ID Type"}))
    id_card = forms.ImageField(label="Id Card", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    signature =  forms.ImageField(label="Signature image", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}))

    class Meta:
        model = Kyc
        fields = ['full_name', 'gender', 'image', 'id_select', 'id_card', 'date_of_birth', 'signature' ] 





#EDIT KYC FORM
class EditKycRegistrationForm(forms.ModelForm):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female")
    )

    MARITAL_CHOICES = (
        ("single", "Single"),
        ("marrried", "Married")
    )

    IDENTITY_CHOICES = (
        ("national id card", "National ID Card"),
        ("drivers licence", "Drivers Licence"),
        ("international passport", "International Passport")
    )

    

    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full name"}))
    marital_status = forms.ChoiceField(choices=MARITAL_CHOICES, widget=forms.Select(attrs={"class":"form-control", "placeholder": "marital status"}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={"class":"form-control", "placeholder": "gender"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "State"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "city"}))
    country = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "country"}))
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "mobile"}))
    image = forms.ImageField(label="Profile Picture", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    id_select = forms.ChoiceField(choices=IDENTITY_CHOICES, widget=forms.Select(attrs={"class":"form-control", "placeholder": "ID Type"}))
    id_card = forms.ImageField(label="Id Card", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    signature =  forms.ImageField(label="Signature image", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date'}))



    class Meta:
        model = Kyc
        fields = ['full_name', 'gender','mobile','country','city','state', 'image', 'id_select', 'id_card', 'date_of_birth', 'signature' ] 





