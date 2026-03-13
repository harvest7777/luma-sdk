import pytest

from core import LumaClient
from core.config import LUMA_API_KEY
from core.models.event import Event
from core.exceptions import ForbiddenError, NotFoundError

@pytest.fixture(scope="session")
def luma_client():
    api_key = LUMA_API_KEY
    return LumaClient(api_key=api_key)
@pytest.mark.vcr
def test_get_event_returns_event(luma_client):
    event = luma_client.get_event("evt-eJuh3dgMEiJ2MUj")
    assert isinstance(event, Event)
    assert event.id == "evt-eJuh3dgMEiJ2MUj"
    assert isinstance(event.name, str)
    assert event.timezone == "America/Los_Angeles"
    assert isinstance(event.hosts, list)
    assert len(event.hosts) > 0

@pytest.mark.vcr
def test_bad_event_raises_forbidden(luma_client):
    with pytest.raises(ForbiddenError):
        luma_client.get_event("evt-xxxxxxxxxxxxxx")

