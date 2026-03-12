from core import LumaClient


def test_client_instantiation():
    client = LumaClient(base_url="https://jsonplaceholder.typicode.com")
    assert client._requester is not None
