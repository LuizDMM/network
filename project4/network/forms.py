from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import User, Post, LikeRelations

class newPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'content', 'dateTime']

    def __init__(self, *args, **kwargs):
        super(newPostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = Textarea(attrs={
            'class': 'form-control',
            'id': 'postContent'
        })