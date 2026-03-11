from core import Client


def test_client_instantiation():
    client = Client(base_url="https://jsonplaceholder.typicode.com")
    assert client._requester is not None
