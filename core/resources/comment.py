from core.base import GithubObject, NotSet


class Comment(GithubObject):
    def _initAttributes(self) -> None:
        self._id = NotSet
        self._post_id = NotSet
        self._name = NotSet
        self._email = NotSet
        self._body = NotSet

    def _useAttributes(self, attributes: dict) -> None:
        if "id" in attributes:
            self._id = int(attributes["id"])
        if "postId" in attributes:
            self._post_id = int(attributes["postId"])
        if "name" in attributes:
            self._name = str(attributes["name"])
        if "email" in attributes:
            self._email = str(attributes["email"])
        if "body" in attributes:
            self._body = str(attributes["body"])

    @property
    def id(self) -> int:
        self._completeIfNotSet(self._id)
        return self._id

    @property
    def post_id(self) -> int:
        self._completeIfNotSet(self._post_id)
        return self._post_id

    @property
    def name(self) -> str:
        self._completeIfNotSet(self._name)
        return self._name

    @property
    def email(self) -> str:
        self._completeIfNotSet(self._email)
        return self._email

    @property
    def body(self) -> str:
        self._completeIfNotSet(self._body)
        return self._body

    def __repr__(self) -> str:
        return f'Comment(id={self._id!r}, email={self._email!r})'
