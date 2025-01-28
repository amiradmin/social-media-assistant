from typing import Type
from django import forms
from .models import Post,SocialMediaAPIKey

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


class APIKeyForm(forms.ModelForm):
    """
    A form for users to input and save their social media API keys.

    This form uses a model form to allow users to input API keys for
    different social media platforms, with the appropriate fields and widgets.

    Attributes:
        Meta (class): Defines the model, fields, and widgets for the form.
    """

    class Meta:
        model = SocialMediaAPIKey
        fields: list[str] = ['platform', 'api_key']
        widgets: dict = {
            'api_key': forms.PasswordInput(attrs={'placeholder': 'Enter your API Key'}),
        }