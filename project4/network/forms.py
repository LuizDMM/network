from django import forms
from django.forms.widgets import Textarea
from .models import User, Post, LikeRelations

class newPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'postContent'})
        }