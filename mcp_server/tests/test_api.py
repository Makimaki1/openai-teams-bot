import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from mcp_server.main import app

client = TestClient(app)


def test_send_message_success():
    with patch('mcp_server.google_chat.send_message', return_value={'id': '1'}) as mock_send:
        resp = client.post('/send_message', json={'space_id': 'abc', 'text': 'hi'})
        assert resp.status_code == 200
        assert resp.json() == {'message': {'id': '1'}}
        mock_send.assert_called_once_with('abc', 'hi')


def test_send_message_error():
    with patch('mcp_server.google_chat.send_message', side_effect=Exception('fail')):
        resp = client.post('/send_message', json={'space_id': 'abc', 'text': 'hi'})
        assert resp.status_code == 500
        assert 'fail' in resp.json()['detail']


def test_fetch_users():
    users = [{'name': 'bob'}]
    with patch('mcp_server.google_chat.fetch_users', return_value=users) as mock_fetch:
        resp = client.post('/fetch_users', json={'space_id': 'abc'})
        assert resp.status_code == 200
        assert resp.json() == {'users': users}
        mock_fetch.assert_called_once_with('abc')


def test_list_channels():
    channels = [{'name': 'space'}]
    with patch('mcp_server.google_chat.list_channels', return_value=channels) as mock_list:
        resp = client.get('/list_channels')
        assert resp.status_code == 200
        assert resp.json() == {'channels': channels}
        mock_list.assert_called_once()

