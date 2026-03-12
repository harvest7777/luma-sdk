import pytest

from core import LumaClient
from core.models.event import Event


@pytest.mark.vcr
def test_get_event_returns_event():
    client = LumaClient(api_key="test-key")
    event = client.get_event("evt-OlQU8n0zzhDZc7A")
    assert isinstance(event, Event)
    assert event.id == "evt-OlQU8n0zzhDZc7A"
    assert event.name == "🎉 AI-Agents Networking + Launch Party! Fetch.ai Innovation Lab"
    assert event.timezone == "America/Los_Angeles"
    assert len(event.hosts) == 6
