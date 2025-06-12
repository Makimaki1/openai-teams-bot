from unittest import mock
import sys
from pathlib import Path

# Ensure repository root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import mcp_server.google_chat as google_chat


def reset_cache():
    google_chat._cached_service = None
    google_chat._cached_credentials = None


def test_get_chat_service_cached(monkeypatch):
    monkeypatch.setattr(google_chat, "SERVICE_ACCOUNT_FILE", "/tmp/key.json")
    reset_cache()
    with mock.patch.object(google_chat.service_account, "Credentials") as cred_cls, \
         mock.patch.object(google_chat, "build") as build_mock:
        cred = mock.Mock()
        cred_cls.from_service_account_file.return_value = cred
        service = mock.Mock()
        build_mock.return_value = service
        s1 = google_chat.get_chat_service()
        s2 = google_chat.get_chat_service()
        assert s1 is s2
        build_mock.assert_called_once()


def test_get_chat_service_refresh(monkeypatch):
    monkeypatch.setattr(google_chat, "SERVICE_ACCOUNT_FILE", "/tmp/key.json")
    reset_cache()
    with mock.patch.object(google_chat.service_account, "Credentials") as cred_cls, \
         mock.patch.object(google_chat, "build") as build_mock:
        cred = mock.Mock()
        cred_cls.from_service_account_file.return_value = cred
        service = mock.Mock()
        build_mock.return_value = service
        google_chat.get_chat_service()
        google_chat.get_chat_service(refresh=True)
        cred.refresh.assert_called_once()
        build_mock.assert_called_once()
