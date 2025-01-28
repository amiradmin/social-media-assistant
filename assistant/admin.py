from django.contrib import admin
from .models import Post
from typing import Type


# Registering the Post model with the admin site
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for managing the 'Post' model.

    This class provides options for how posts should be displayed and
    interacted with in the Django admin panel.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view.
        search_fields (tuple): Allows search functionality based on the specified fields.
        list_filter (tuple): Enables filtering posts by the specified fields.
    """

    # Fields to display in the list view
    list_display = ('title', 'content', 'hashtags', 'created_at')

    # Fields to allow search functionality
    search_fields = ('title', 'content', 'hashtags')

    # Fields to enable filtering by
    list_filter = ('created_at',)