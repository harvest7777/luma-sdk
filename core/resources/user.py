from __future__ import annotations

from core.base import GithubObject, NotSet
from core.resources.post import Post


class User(GithubObject):
    def _initAttributes(self) -> None:
        self._id = NotSet
        self._name = NotSet
        self._username = NotSet
        self._email = NotSet
        self._phone = NotSet
        self._website = NotSet
        self._address = NotSet
        self._company = NotSet

    def _useAttributes(self, attributes: dict) -> None:
        if "id" in attributes:
            self._id = int(attributes["id"])
        if "name" in attributes:
            self._name = str(attributes["name"])
        if "username" in attributes:
            self._username = str(attributes["username"])
        if "email" in attributes:
            self._email = str(attributes["email"])
        if "phone" in attributes:
            self._phone = str(attributes["phone"])
        if "website" in attributes:
            self._website = str(attributes["website"])
        if "address" in attributes:
            self._address = dict(attributes["address"])
        if "company" in attributes:
            self._company = dict(attributes["company"])

    @property
    def id(self) -> int:
        self._completeIfNotSet(self._id)
        return self._id

    @property
    def name(self) -> str:
        self._completeIfNotSet(self._name)
        return self._name

    @property
    def username(self) -> str:
        self._completeIfNotSet(self._username)
        return self._username

    @property
    def email(self) -> str:
        self._completeIfNotSet(self._email)
        return self._email

    @property
    def phone(self) -> str:
        self._completeIfNotSet(self._phone)
        return self._phone

    @property
    def website(self) -> str:
        self._completeIfNotSet(self._website)
        return self._website

    @property
    def address(self) -> dict:
        self._completeIfNotSet(self._address)
        return self._address

    @property
    def company(self) -> dict:
        self._completeIfNotSet(self._company)
        return self._company

    def get_posts(self) -> list[Post]:
        """GET /users/{id}/posts — returns all posts by this user."""
        raw = self._requester.request_json_and_check("GET", f"{self._url}/posts")
        return [
            Post(self._requester, f"/posts/{item['id']}", attributes=item)
            for item in raw
        ]

    def __repr__(self) -> str:
        return f'User(id={self._id!r}, username={self._username!r})'
