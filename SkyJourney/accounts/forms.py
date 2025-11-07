# this file is for building custom forms.

# importing the User model from django's inbuilt authentication app
from django.contrib.auth.models import User 

# importing the inbuilt forms
from django import forms

# import AuthenticationForm from django's inbuilt authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget= forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter your username'
        })
    )

    password = forms.CharField(
        label = 'Password',
        widget= forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter your password'
        })
    )

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username','email','password1','password2')
    email = forms.EmailField(
        widget= forms.EmailInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter your email'
        })
    )
    username = forms.CharField(
        widget= forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter your username',
            
        })
    )

    password1 = forms.CharField(
        label = 'Password',
        widget= forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Enter your password'
        })
    )

    password2 = forms.CharField(
        label = 'Confirm Password',
        widget= forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Confirm Password'
        })
    )

    