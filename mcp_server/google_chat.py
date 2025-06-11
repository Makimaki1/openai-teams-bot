"""Wrapper functions for interacting with Google Chat."""
from typing import List
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/chat.bot",
    "https://www.googleapis.com/auth/chat.readonly",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
]

SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")


def get_chat_service():
    """Return an authorized Google Chat service client."""
    if not SERVICE_ACCOUNT_FILE:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE env var not set")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("chat", "v1", credentials=credentials)


def send_message(space_id: str, text: str) -> dict:
    """Send a message to a Google Chat space."""
    service = get_chat_service()
    return (
        service.spaces()
        .messages()
        .create(parent=f"spaces/{space_id}", body={"text": text})
        .execute()
    )


def list_channels() -> List[dict]:
    """List spaces available to the bot."""
    service = get_chat_service()
    resp = service.spaces().list().execute()
    return resp.get("spaces", [])


def fetch_users(space_id: str) -> List[dict]:
    """Fetch members in a space."""
    service = get_chat_service()
    resp = service.spaces().members().list(parent=f"spaces/{space_id}").execute()
    return resp.get("memberships", [])
