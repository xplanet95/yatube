from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['text', 'group', 'image']
        # widgets = {
        #     'text': forms.Textarea(),
        #     'group': forms.Select(),
        # }
            # attrs = {'class': 'form-control'}