import pytest
from core.requester import Requester


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

def test_construct_url():
    req = Requester(base_url="https://public-api.luma.com")
    assert req._construct_url("/events") == "https://public-api.luma.com/events"

def test_construct_url_adds_leading_slash():
    req = Requester(base_url="https://public-api.luma.com")
    assert req._construct_url("events") == "https://public-api.luma.com/events"

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


@pytest.mark.vcr
def test_successful_request_returns_data():
    req = Requester(base_url="https://jsonplaceholder.typicode.com")
    data = req.request_json_and_check("GET", "/todos/1")
    assert data["id"] == 1
