"""Wrapper functions for interacting with Google Chat."""
from typing import List
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

from fastapi.concurrency import run_in_threadpool
=======
from google.auth.transport.requests import Request


SCOPES = [
    "https://www.googleapis.com/auth/chat.bot",
    "https://www.googleapis.com/auth/chat.readonly",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
]

SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
_CHAT_SERVICE = None


def get_chat_service():
    """Return an authorized Google Chat service client."""
    global _CHAT_SERVICE
    if _CHAT_SERVICE is None:
        if not SERVICE_ACCOUNT_FILE:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE env var not set")
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        _CHAT_SERVICE = build("chat", "v1", credentials=credentials)
    return _CHAT_SERVICE

_cached_service = None
_cached_credentials = None


def get_chat_service(refresh: bool = False):
    """Return an authorized Google Chat service client.

    Caches the service instance for reuse. Pass ``refresh=True`` to
    refresh the underlying credentials token.
    """
    global _cached_service, _cached_credentials

    if not SERVICE_ACCOUNT_FILE:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE env var not set")

    if _cached_service is None or _cached_credentials is None:
        _cached_credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        _cached_service = build("chat", "v1", credentials=_cached_credentials)
    elif refresh:
        _cached_credentials.refresh(Request())

    return _cached_service



def send_message(space_id: str, text: str) -> dict:
    """Send a message to a Google Chat space."""
    service = get_chat_service()
    return (
        service.spaces()
        .messages()
        .create(parent=f"spaces/{space_id}", body={"text": text})
        .execute()
    )


async def send_message_async(space_id: str, text: str) -> dict:
    """Async wrapper for send_message using a thread pool."""
    return await run_in_threadpool(send_message, space_id, text)


def list_channels() -> List[dict]:
    """List spaces available to the bot."""
    service = get_chat_service()
    resp = service.spaces().list().execute()
    return resp.get("spaces", [])


async def list_channels_async() -> List[dict]:
    """Async wrapper for list_channels using a thread pool."""
    return await run_in_threadpool(list_channels)


def fetch_users(space_id: str) -> List[dict]:
    """Fetch members in a space."""
    service = get_chat_service()
    resp = service.spaces().members().list(parent=f"spaces/{space_id}").execute()
    return resp.get("memberships", [])


async def fetch_users_async(space_id: str) -> List[dict]:
    """Async wrapper for fetch_users using a thread pool."""
    return await run_in_threadpool(fetch_users, space_id)
