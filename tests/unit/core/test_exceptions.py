import pytest
import requests
from luma_sdk.sdk_models.requester import Requester
from luma_sdk.sdk_models.exceptions import (
    TransientError,
    ServerError,
    RateLimitError,
    RequestTimeoutError,
    NetworkError,
)


def test_server_error_is_transient():
    assert isinstance(ServerError(500), TransientError)


def test_rate_limit_error_is_transient():
    assert isinstance(RateLimitError(429), TransientError)


def test_request_timeout_error_is_transient():
    assert isinstance(RequestTimeoutError(), TransientError)


def test_network_error_is_transient():
    assert isinstance(NetworkError(), TransientError)


def test_connection_error_raises_network_error():
    req = Requester("https://api.test")

    class ConnectionErrorSession:
        def request(self, *args, **kwargs):
            raise requests.exceptions.ConnectionError()

    req._session = ConnectionErrorSession()
    with pytest.raises(NetworkError):
        req.get("/events")
