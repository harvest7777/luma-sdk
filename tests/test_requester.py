import pytest

from core.exceptions import NotFoundError
from core.requester import Requester


@pytest.fixture
def requester():
    return Requester(base_url="https://jsonplaceholder.typicode.com")


@pytest.mark.vcr
def test_get_returns_parsed_json(requester):
    data = requester.request_json_and_check("GET", "/posts/1")
    assert data["id"] == 1


@pytest.mark.vcr
def test_raises_not_found_on_404(requester):
    with pytest.raises(NotFoundError) as exc_info:
        requester.request_json_and_check("GET", "/posts/9999")
    assert exc_info.value.status == 404
