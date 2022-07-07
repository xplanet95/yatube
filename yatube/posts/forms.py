from django import forms
from .models import Post, Comment, Follow


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


# class CommentForm(forms.Form):
#     text = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['user', ]
