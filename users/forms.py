from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User

class UserLoginForm(AuthenticationForm):

    class Meta():
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class ProfileForm(UserChangeForm):
    class Meta():
        model = User
        fields = (
            'image', 
            'username',
            'email',)
            
    image = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.CharField()