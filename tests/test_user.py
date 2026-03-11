import pytest

from core import Luma


@pytest.mark.vcr
def test_get_user():
    client = Luma()
    user = client.get_user(1)
    # First property access triggers lazy GET /users/1
    assert user.id == 1
    assert user.name == "Leanne Graham"
    assert user.username == "Bret"
    assert user.email == "Sincere@april.biz"
    assert user.address["city"] == "Gwenborough"
    assert user.address["geo"]["lat"] == "-37.3159"
    assert user.company["name"] == "Romaguera-Crona"


@pytest.mark.vcr
def test_get_user_posts():
    client = Luma()
    user = client.get_user(1)
    # get_posts() calls GET /users/1/posts directly — no lazy fetch needed
    posts = user.get_posts()
    assert len(posts) == 10
    assert posts[0].id == 1
    assert posts[0].title == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
    assert posts[9].id == 10
    assert posts[9].title == "optio molestias id quia eum"
