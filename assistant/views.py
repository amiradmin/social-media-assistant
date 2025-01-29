from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm,APIKeyForm
from typing import Type
from .models import SocialMediaAPIKey
from utils.linkedin_connector import post_to_linkedin  # Import the LinkedIn function
from utils.linkedin_connector import get_access_token, post_to_linkedin
import requests
import os


# Load environment variables
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
REDIRECT_URI = "http://127.0.0.1:8000/assistant/linkedin/callback/"
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")


def linkedin_auth(request):
    """
    Redirects the user to LinkedIn's authorization page.
    """
    auth_url = (
        f"{LINKEDIN_AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=w_member_social"
    )
    return redirect(auth_url)


def linkedin_callback(request):
    """
    Handles LinkedIn OAuth callback and exchanges the authorization code for an access token.
    """
    code = request.GET.get("code")

    if not code:
        return render(request, "social_media/error.html", {"message": "Authorization failed."})

    try:
        access_token = get_access_token(code)
        request.session["linkedin_access_token"] = access_token  # Store token in session
        return redirect("create_post")  # Redirect to post creation page
    except Exception as e:
        return render(request, "social_media/error.html", {"message": str(e)})


def create_post(request):
    """
    Handles post creation and optionally posts to LinkedIn.
    """
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()

            access_token = request.session.get("linkedin_access_token")
            if access_token:
                success = post_to_linkedin(access_token, post.content)
                if success:
                    print("Successfully posted to LinkedIn!")
                else:
                    print("Failed to post to LinkedIn.")

            return redirect("post_success")

    else:
        form = PostForm()

    return render(request, "social_media/create_post.html", {"form": form})



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