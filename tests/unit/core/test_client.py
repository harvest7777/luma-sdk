from luma_sdk import *

def test_client_instantiation():
    client = LumaClient(api_key="test-key")
    assert client._requester is not None

def test_get_events_returns_paginated_list():
    client = LumaClient(api_key="test-key")
    result = client.get_events()
    assert isinstance(result, PaginatedList)
