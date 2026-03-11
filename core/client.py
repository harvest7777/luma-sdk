from core.requester import Requester


class Client:
    """
    Base entry point for an SDK. Owns the Requester and wires it to resources.

    To build an SDK from this scaffold:
      1. Subclass or configure Client with your API's base_url
      2. Add methods that return Resource instances, e.g.:
           def get_post(self, post_id: int) -> Post:
               return Post(self._requester, f"/posts/{post_id}")
    """

    def __init__(self, base_url: str, timeout: int = Requester.DEFAULT_TIMEOUT) -> None:
        self._requester = Requester(base_url=base_url, timeout=timeout)
