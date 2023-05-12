from django import forms
from blog.models import Post

class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'photo', 'body', 'tags', 'category')
