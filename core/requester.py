import requests

from core.exceptions import (
    BadRequestException,
    LumaException,
    ServerErrorException,
    UnknownObjectException,
)


class Requester:
    DEFAULT_BASE_URL = "https://jsonplaceholder.typicode.com"
    DEFAULT_TIMEOUT = 10
    DEFAULT_USER_AGENT = "luma-sdk/0.1.0"

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept": "application/json",
            }
        )

    def request_json(
        self,
        verb: str,
        path: str,
        parameters: dict | None = None,
    ) -> tuple[int, dict | list]:
        """Make an HTTP request. Returns (status_code, parsed_body)."""
        url = f"{self._base_url}{path}"
        response = self._session.request(
            method=verb,
            url=url,
            params=parameters,
            timeout=self._timeout,
        )
        try:
            data = response.json()
        except ValueError:
            data = {}
        return response.status_code, data

    def request_json_and_check(
        self,
        verb: str,
        path: str,
        parameters: dict | None = None,
    ) -> dict | list:
        """Like request_json but raises LumaException on non-2xx responses."""
        status, data = self.request_json(verb, path, parameters)
        self._check(status, data)
        return data

    @staticmethod
    def _check(status: int, data: object) -> None:
        if status == 404:
            raise UnknownObjectException(status, data)
        if 400 <= status < 500:
            raise BadRequestException(status, data)
        if status >= 500:
            raise ServerErrorException(status, data)
