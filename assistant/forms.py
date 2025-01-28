from typing import Type
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    A form for creating and updating Post objects.

    This form is based on the Post model and includes the following fields:
    - title
    - content
    - hashtags
    - image
    """
    class Meta:
        model: Type[Post] = Post
        fields: list[str] = ['title', 'content', 'hashtags', 'image']