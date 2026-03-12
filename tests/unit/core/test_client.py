from unittest.mock import MagicMock

import pytest

from core import LumaClient
from core.models.event import Event


def test_client_instantiation():
    client = LumaClient(api_key="test-key")
    assert client._requester is not None


def test_get_event_calls_correct_path_and_returns_event(event_api_response):
    client = LumaClient(api_key="test-key")
    client._requester.get = MagicMock(return_value=event_api_response)

    result = client.get_event("evt-OlQU8n0zzhDZc7A")

    client._requester.get.assert_called_once_with(
        "/event/get", parameters={"id": "evt-OlQU8n0zzhDZc7A"}
    )
    assert isinstance(result, Event)
    assert result.id == "evt-OlQU8n0zzhDZc7A"
    assert result.name == "Test Event"
