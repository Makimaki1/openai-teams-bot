"""Wrapper functions for interacting with Google Chat."""
from typing import List
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fastapi.concurrency import run_in_threadpool
=======
from google.auth.transport.requests import Request


SCOPES = [
    "https://www.googleapis.com/auth/chat.bot",
    "https://www.googleapis.com/auth/chat.readonly",
    "https://www.googleapis.com/auth/chat.memberships.readonly",
    "https://www.googleapis.com/auth/admin.directory.group.readonly",
    "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
]

SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")

ADMIN_SUBJECT = os.environ.get("GOOGLE_ADMIN_SUBJECT")
=======
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


def get_directory_service():
    """Return an authorized Admin SDK Directory service client."""
    if not SERVICE_ACCOUNT_FILE:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE env var not set")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    if ADMIN_SUBJECT:
        credentials = credentials.with_subject(ADMIN_SUBJECT)
    return build("admin", "directory_v1", credentials=credentials)


def is_group_member(user_email: str, group_email: str) -> bool:
    """Return True if the user is a member of the group."""
    service = get_directory_service()
    try:
        service.members().get(groupKey=group_email, memberKey=user_email).execute()
        return True
    except HttpError as exc:
        if exc.resp.status == 404:
            return False
        raise


def list_group_members(group_email: str) -> List[dict]:
    """Return the members of a Google Group."""
    service = get_directory_service()
    resp = service.members().list(groupKey=group_email).execute()
    return resp.get("members", [])

async def fetch_users_async(space_id: str) -> List[dict]:
    """Async wrapper for fetch_users using a thread pool."""
    return await run_in_threadpool(fetch_users, space_id)

