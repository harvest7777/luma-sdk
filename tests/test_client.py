import pytest

from core import Luma
from core.resources.post import Post
from core.resources.user import User


def test_client_instantiation():
    # No network call — just object creation
    client = Luma()
    assert client is not None


@pytest.mark.vcr
def test_client_get_post():
    client = Luma()
    post = client.get_post(1)
    assert isinstance(post, Post)
    assert post.id == 1  # lazy fetch fires here


@pytest.mark.vcr
def test_client_get_user():
    client = Luma()
    user = client.get_user(1)
    assert isinstance(user, User)
    assert user.id == 1  # lazy fetch fires here
