from django import forms
from .models import *

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title','slug','content','cat']