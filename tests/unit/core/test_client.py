from core import LumaClient


def test_client_instantiation():
    client = LumaClient(base_url="https://public-api.luma.com", api_key="test-key")
    assert client._requester is not None
