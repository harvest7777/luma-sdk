from core import LumaClient


def test_client_instantiation():
    client = LumaClient(api_key="test-key")
    assert client._requester is not None
