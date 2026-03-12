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


