import pytest
from luma_sdk.config import LUMA_API_KEY
from luma_sdk import LumaClient, PaginatedList


@pytest.fixture(scope="session")
def luma_client():
    api_key = LUMA_API_KEY
    return LumaClient(api_key=api_key)

def test_client_instantiation():
    client = LumaClient(api_key="test-key")
    assert client._requester is not None

def test_get_events_returns_paginated_list(luma_client):
    result = luma_client.get_events()
    assert isinstance(result, PaginatedList)
