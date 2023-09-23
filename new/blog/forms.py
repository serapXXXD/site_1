from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'photo',
            'body',
            'tags',
            'category',
        )
        widgets = {
            'tags': forms.Select(attrs={'multiple': True})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
