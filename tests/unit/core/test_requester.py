import pytest
import requests
from luma_sdk.requester import Requester
from luma_sdk.exceptions import ClientError, ForbiddenError, NotFoundError, RateLimitError, ServerError, RequestTimeoutError


def test_requester_init():
    req = Requester(base_url="https://public-api.luma.com")
    assert req._base_url == "https://public-api.luma.com"

def test_requester_init_trailing_slash():
    req = Requester(base_url="https://public-api.luma.com/")
    assert req._base_url == "https://public-api.luma.com"

def test_reqester_no_https_raises_exception():
    with pytest.raises(ValueError):
        Requester(base_url="public-api.luma.com")

def test_requester_omits_white_spaces():
    req = Requester(base_url="  https://public-api.luma.com/  ")
    assert req._base_url == "https://public-api.luma.com"

def test_construct_url_adds_leading_slash():
    req = Requester("https://api.test")
    assert req._construct_url("events") == "https://api.test/events"


def test_construct_url_preserves_leading_slash():
    req = Requester("https://api.test")
    assert req._construct_url("/events") == "https://api.test/events"
def test_base_url_must_be_https():
    with pytest.raises(ValueError):
        Requester("http://insecure.com")

def test_construct_url_omits_white_spaces():
    req = Requester(base_url="https://public-api.luma.com")
    assert req._construct_url(" events ") == "https://public-api.luma.com/events"

def test_custom_headers_update_session():
    req = Requester(
        base_url="https://public-api.luma.com",
        headers={"x-luma-api-key": "test-key"},
    )
    assert req._session.headers["x-luma-api-key"] == "test-key"

def test_no_custom_headers_keeps_defaults():
    req = Requester(base_url="https://public-api.luma.com")
    assert req._session.headers["Accept"] == "application/json"
    assert "x-luma-api-key" not in req._session.headers


def test_check_200_does_not_raise():
    Requester._check(200, {})


def test_check_404_raises_not_found():
    with pytest.raises(NotFoundError):
        Requester._check(404, {})


def test_check_403_raises_forbidden():
    with pytest.raises(ForbiddenError):
        Requester._check(403, {})


def test_check_429_raises_rate_limit_error():
    with pytest.raises(RateLimitError):
        Requester._check(429, {})

def test_check_4xx_raises_client_error():
    with pytest.raises(ClientError):
        Requester._check(400, {})


def test_check_5xx_raises_server_error():
    with pytest.raises(ServerError):
        Requester._check(500, {})


def test_timeout_raises_timeout_error():
    req = Requester("https://api.test")

    class TimeoutSession:
        def request(self, *args, **kwargs):
            raise requests.exceptions.Timeout()

    req._session = TimeoutSession()
    with pytest.raises(RequestTimeoutError):
        req.get("/events")

def test_post_timeout_raises_timeout_error():
    req = Requester("https://api.test")

    class TimeoutSession:
        def request(self, *args, **kwargs):
            raise requests.exceptions.Timeout()

    req._session = TimeoutSession()
    with pytest.raises(RequestTimeoutError):
        req.post("/events")