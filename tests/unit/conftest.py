import pytest


@pytest.fixture
def event_api_response():
    return {
        "event": {
            "api_id": "evt-OlQU8n0zzhDZc7A",
            "calendar_api_id": "cal-G6RucUfw1nBs8qT",
            "user_api_id": "usr-Tw1bycXxO8mdP8w",
            "name": "Test Event",
            "description": "A test event.",
            "description_md": None,
            "cover_url": None,
            "url": "https://luma.com/test",
            "start_at": "2024-08-24T02:00:00.000Z",
            "end_at": "2024-08-24T05:00:00.000Z",
            "timezone": "America/Los_Angeles",
            "visibility": "public",
            "geo_address_json": None,
            "tags": [],
        },
        "hosts": [],
    }
