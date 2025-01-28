from django.db import models

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