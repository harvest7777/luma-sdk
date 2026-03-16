import pytest
from luma_sdk.requester import Requester


@pytest.mark.vcr
def test_successful_request_returns_data():
    req = Requester(base_url="https://jsonplaceholder.typicode.com")
    data = req._request_json_and_check("GET", "/todos/1")
    assert data["id"] == 1

@pytest.mark.vcr
def test_request_with_x_api_key_header_returns_success():
    req = Requester(
        base_url="https://jsonplaceholder.typicode.com",
        headers={"x-luma-api-key": "test-key"},
    )
    data = req._request_json_and_check("GET", "/posts/10")
    assert data["id"] == 10

@pytest.mark.vcr
def test_post_returns_data():
    req = Requester(base_url="https://jsonplaceholder.typicode.com")
    data = req.post("/posts", body={"title": "foo", "body": "bar", "userId": 1})
    assert data["title"] == "foo"
    assert data["userId"] == 1
