import os

import pytest

from luma_sdk import *


@pytest.fixture(scope="session")
def luma_client():
    return LumaClient(api_key=os.getenv("LUMA_API_KEY"))

@pytest.fixture(scope="session")
def test_luma_client():
    return LumaClient(api_key=os.getenv("TEST_LUMA_API_KEY"))
@pytest.mark.vcr
def test_get_event_returns_event(luma_client):
    event = luma_client.get_event("evt-eJuh3dgMEiJ2MUj")
    assert isinstance(event, Event)
    assert event.id == "evt-eJuh3dgMEiJ2MUj"
    assert isinstance(event.name, str)
    assert event.timezone == "America/Los_Angeles"
    assert event.geo_address

@pytest.mark.vcr
def test_bad_event_raises_forbidden(luma_client):
    with pytest.raises(ForbiddenError):
        luma_client.get_event("evt-xxxxxxxxxxxxxx")

@pytest.mark.vcr
def test_get_events_returns_only_event_types(luma_client):
    events = luma_client.get_events()
    assert all(isinstance(e, Event) for e in events)

@pytest.mark.vcr
def test_get_guest_returns_guest(luma_client):
    event = luma_client.get_event("evt-OlQU8n0zzhDZc7A")
    guest = event.get_guest("gst-RfpTVyE4hInUucp")
    assert isinstance(guest, Guest)
    assert guest.id == "gst-RfpTVyE4hInUucp"
    assert isinstance(guest.user_email, str)
    assert guest.approval_status in {"approved", "session", "pending_approval", "invited", "declined", "waitlist"}

@pytest.mark.vcr
def test_get_guests_returns_paginated_list_of_guests(luma_client):
    event = luma_client.get_event("evt-OlQU8n0zzhDZc7A")
    guests = event.get_guests()
    assert all(isinstance(g, Guest) for g in guests)

@pytest.mark.vcr
def test_add_guests_returns_none_on_success(test_luma_client):
    from luma_sdk.models.event import GuestInput
    event = test_luma_client.get_event("evt-DXHV4IC8LpKP9c3")
    guest = event.add_guests([GuestInput(email="test@example.com", name="Test User")])
    assert guest is None


