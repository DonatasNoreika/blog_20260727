from .models import CustomUser, Comment
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
