import requests

from core.exceptions import ApiError, ClientError, NotFoundError, ServerError


class Requester:
    DEFAULT_TIMEOUT = 10

    def __init__(
        self,
        base_url: str,
        timeout: int = DEFAULT_TIMEOUT,
        headers: dict | None = None,
    ) -> None:
        base_url = base_url.strip().rstrip("/")
        if not base_url.startswith("https://"):
            raise ValueError(f"base_url must start with 'https://', got: {base_url!r}")
        self._base_url = base_url
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})
        if headers:
            self._session.headers.update(headers)

    # Combines base_url and a resource path into a full request URL.
    def _construct_url(self, path: str) -> str:
        path = path.strip()
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self._base_url}{path}"

    def _request_json(
        self,
        verb: str,
        path: str,
        parameters: dict | None = None,
    ) -> tuple[int, dict | list]:
        url = self._construct_url(path)
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
        status, data = self._request_json(verb, path, parameters)
        self._check(status, data)
        return data

    @staticmethod
    def _check(status: int, data: object) -> None:
        if status == 404:
            raise NotFoundError(status, data)
        if 400 <= status < 500:
            raise ClientError(status, data)
        if status >= 500:
            raise ServerError(status, data)
