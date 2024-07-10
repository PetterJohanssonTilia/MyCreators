from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Creator

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreatorRequestForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['creator_type', 'request_message']
        widgets = {
            'request_message': forms.Textarea(attrs={'rows': 4}),
        }