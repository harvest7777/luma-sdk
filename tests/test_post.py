import pytest

from core import Luma


@pytest.mark.vcr
def test_get_post():
    client = Luma()
    post = client.get_post(1)
    # First property access triggers lazy GET /posts/1
    assert post.id == 1
    assert post.user_id == 1
    assert post.title == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert post.body.startswith("quia et suscipit")


@pytest.mark.vcr
def test_get_post_comments():
    client = Luma()
    post = client.get_post(1)
    # get_comments() calls GET /posts/1/comments directly — no lazy fetch needed
    comments = post.get_comments()
    assert len(comments) == 5
    assert comments[0].id == 1
    assert comments[0].post_id == 1
    assert comments[0].email == "Eliseo@gardner.biz"
    assert comments[4].name == "vero eaque aliquid doloribus et culpa"
