class ApiError(Exception):
    def __init__(self, status: int, data: object = None) -> None:
        self.status = status
        self.data = data
        super().__init__(f"{status} {data}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.status}, {self.data!r})"


class NotFoundError(ApiError):
    """Raised on 404."""


class EventNotFoundError(NotFoundError):
    """Raised when a specific event cannot be found."""


class GuestNotFoundError(NotFoundError):
    """Raised when a specific guest cannot be found."""


class ForbiddenError(ApiError):
    """Raised on 403."""


class ClientError(ApiError):
    """Raised on 4xx errors other than 403 and 404."""


class ServerError(ApiError):
    """Raised on 5xx errors."""


class RequestTimeoutError(Exception):
    """Raised when a request times out."""
