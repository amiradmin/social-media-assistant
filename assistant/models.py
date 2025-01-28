from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Represents a social media post created by a user.

    Attributes:
        title (str): The title of the post, limited to 200 characters.
        content (str): The main text content of the post.
        hashtags (str): A comma-separated string of hashtags for the post, optional.
        image (ImageField): An optional image associated with the post, stored in the 'posts_images/' directory.
        created_at (DateTime): The date and time when the post was created. Automatically set upon creation.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    hashtags = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='posts_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the Post instance.

        Returns:
            str: The title of the post.
        """
        return self.title



class SocialMediaAPIKey(models.Model):
    """
    Represents an API key for a specific social media platform associated with a user.

    Attributes:
        PLATFORM_CHOICES (list[tuple[str, str]]): Choices for supported platforms.
        user (models.ForeignKey): A reference to the user who owns the API key.
        platform (models.CharField): The social media platform (LinkedIn, Instagram, or Twitter).
        api_key (models.CharField): The API key associated with the platform.
        created_at (models.DateTimeField): Timestamp indicating when the key was created.
    """
    PLATFORM_CHOICES: list[tuple[str, str]] = [
        ('LinkedIn', 'LinkedIn'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
    ]

    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user who owns this API key.",
    )
    platform: models.CharField = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        help_text="The platform for which this API key is valid (LinkedIn, Instagram, Twitter).",
    )
    api_key: models.CharField = models.CharField(
        max_length=255,
        help_text="The API key for accessing the social media platform.",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the API key was created.",
    )

    def __str__(self) -> str:
        """
        Returns:
            str: A string representation of the API key, including the username and platform.
        """
        return f"{self.user.username} - {self.platform}"
