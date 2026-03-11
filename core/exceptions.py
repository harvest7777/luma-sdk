class LumaException(Exception):
    """Base exception for all SDK errors."""

    def __init__(self, status: int, data: object = None) -> None:
        self.status = status
        self.data = data
        super().__init__(f"{status} {data}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.status}, {self.data!r})"


class UnknownObjectException(LumaException):
    """Raised on 404 — resource does not exist."""


class BadRequestException(LumaException):
    """Raised on 4xx errors other than 404."""


class ServerErrorException(LumaException):
    """Raised on 5xx errors."""
