from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Creator, Post
from django_summernote.widgets import SummernoteWidget

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreatorRequestForm(forms.Form):
    CREATOR_TYPES = [
        ('PHOTOGRAPHER', 'Photographer'),
        ('GAME_DEVELOPER', 'Game Developer'),
        ('CONTENT_CREATOR', 'Content Creator'),
        ('ARTIST', 'Artist'),
        ('VOICE_ACTOR', 'Voice Actor'),
        ('OTHER', 'Other'),
    ]
    creator_type = forms.ChoiceField(choices=CREATOR_TYPES)
    request_message = forms.CharField(widget=forms.Textarea)


class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['avatar', 'creator_type', 'about_me']
        widgets = {
            'about_me': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator_type'].choices = CreatorRequestForm.CREATOR_TYPES

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }