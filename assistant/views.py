from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm
from typing import Type


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