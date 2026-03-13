import pytest

from luma_sdk import LumaClient, PaginatedList
from luma_sdk.config import LUMA_API_KEY
from luma_sdk.models.event import Event
from luma_sdk.exceptions import ForbiddenError, NotFoundError

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

@pytest.mark.vcr
def test_bad_event_raises_forbidden(luma_client):
    with pytest.raises(ForbiddenError):
        luma_client.get_event("evt-xxxxxxxxxxxxxx")

@pytest.mark.vcr
def test_get_events_returns_only_event_types(luma_client):
    events = luma_client.get_events()
    assert all(isinstance(e, Event) for e in events)


