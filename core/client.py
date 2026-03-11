from core.requester import Requester
from core.resources.post import Post
from core.resources.user import User


class Luma:
    """
    Entry point for the Luma SDK.

    Usage:
        client = Luma()
        post = client.get_post(1)
        print(post.title)           # lazy GET /posts/1 on first access
        comments = post.get_comments()
    """

    def __init__(
        self,
        base_url: str = Requester.DEFAULT_BASE_URL,
        timeout: int = Requester.DEFAULT_TIMEOUT,
    ) -> None:
        self.__requester = Requester(base_url=base_url, timeout=timeout)

    def get_post(self, post_id: int) -> Post:
        """Return a Post shell for the given ID. Data is fetched lazily."""
        return Post(self.__requester, f"/posts/{post_id}")

    def get_user(self, user_id: int) -> User:
        """Return a User shell for the given ID. Data is fetched lazily."""
        return User(self.__requester, f"/users/{user_id}")
