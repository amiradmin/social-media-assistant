from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm,APIKeyForm
from typing import Type
from .models import SocialMediaAPIKey



def create_post(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a new post.

    If the request method is POST, it processes the submitted form data.
    If the form is valid, the post is saved, and the user is redirected to the success page.
    If the request method is GET, it displays an empty form for creating a post.

    Args:
        request (HttpRequest): The HTTP request object containing request data.

    Returns:
        HttpResponse: The HTTP response object rendering the post creation form
        or redirecting to the success page upon successful form submission.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_success')  # Redirect to a success page or the post list
    else:
        form = PostForm()

    return render(request, 'social_media/create_post.html', {'form': form})



def post_success(request: Type[HttpRequest]) -> Type[HttpResponse]:
    """
    View for displaying a success page after a post is created.

    This view renders a template that confirms the successful creation
    of a post and is typically used after a post is saved.

    Args:
        request (HttpRequest): The HTTP request object, containing metadata
                               about the request, such as headers and GET/POST data.

    Returns:
        HttpResponse: The rendered template response that shows the success message.
    """
    return render(request, 'social_media/post_success.html')


def settings_menu(request: HttpRequest) -> HttpResponse:
    """
    Displays the settings menu where users can add and view their social media API keys.

    If the request method is POST, the form is validated and the API key is saved to the database.
    If the request method is GET, the form is displayed, and any existing API keys for the user are retrieved.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered HTML response, displaying the settings menu with the form and existing API keys.
    """
    if request.method == 'POST':
        form = APIKeyForm(request.POST)
        if form.is_valid():
            api_key_instance = form.save(commit=False)
            api_key_instance.user = request.user  # Assign the logged-in user
            api_key_instance.save()
            return redirect('settings_menu')  # Redirect to the same page after saving
    else:
        form = APIKeyForm()

    user_keys = SocialMediaAPIKey.objects.filter(user=request.user)  # Show user's keys

    return render(request, 'social_media/settings_menu.html', {
        'form': form,
        'user_keys': user_keys,
    })