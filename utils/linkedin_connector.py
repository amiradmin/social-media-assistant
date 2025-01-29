import os
import requests
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/assistant/linkedin/callback/"  # Update as needed
ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
POST_URL = "https://api.linkedin.com/v2/ugcPosts"


def get_access_token(authorization_code: str) -> str:
    """
    Exchange the authorization code for an access token.

    Args:
        authorization_code (str): The authorization code received from LinkedIn.

    Returns:
        str: The access token.
    """
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }
    response = requests.post(ACCESS_TOKEN_URL, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error fetching access token: {response.text}")


def post_to_linkedin(access_token: str, content: str) -> bool:
    """
    Publish a post on LinkedIn.

    Args:
        access_token (str): The LinkedIn API access token.
        content (str): The content of the post.

    Returns:
        bool: True if successful, False otherwise.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    user_info_url = "https://api.linkedin.com/v2/me"
    user_response = requests.get(user_info_url, headers=headers)

    if user_response.status_code != 200:
        print("Error fetching user info:", user_response.text)
        return False

    user_id = user_response.json().get("id")

    data = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(POST_URL, headers=headers, json=data)

    return response.status_code == 201
