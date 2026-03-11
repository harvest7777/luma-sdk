from __future__ import annotations

from core.base import GithubObject, NotSet
from core.resources.comment import Comment


class Post(GithubObject):
    def _initAttributes(self) -> None:
        self._id = NotSet
        self._user_id = NotSet
        self._title = NotSet
        self._body = NotSet

    def _useAttributes(self, attributes: dict) -> None:
        if "id" in attributes:
            self._id = int(attributes["id"])
        if "userId" in attributes:
            self._user_id = int(attributes["userId"])
        if "title" in attributes:
            self._title = str(attributes["title"])
        if "body" in attributes:
            self._body = str(attributes["body"])

    @property
    def id(self) -> int:
        self._completeIfNotSet(self._id)
        return self._id

    @property
    def user_id(self) -> int:
        self._completeIfNotSet(self._user_id)
        return self._user_id

    @property
    def title(self) -> str:
        self._completeIfNotSet(self._title)
        return self._title

    @property
    def body(self) -> str:
        self._completeIfNotSet(self._body)
        return self._body

    def get_comments(self) -> list[Comment]:
        """GET /posts/{id}/comments — returns all comments for this post."""
        raw = self._requester.request_json_and_check("GET", f"{self._url}/comments")
        return [
            Comment(self._requester, f"/comments/{item['id']}", attributes=item)
            for item in raw
        ]

    def __repr__(self) -> str:
        return f'Post(id={self._id!r}, title={self._title!r})'
