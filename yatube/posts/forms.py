from django import forms
from .models import Post


class PostForm(forms.Form):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['text', 'group']
        widgets = {
            'text': forms.TextInput(),
            'group': forms.Select(),
        }
            # attrs = {'class': 'form-control'}