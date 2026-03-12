from core.requester import Requester


class LumaClient:
    """
    Base entry point for an SDK. Owns the Requester and wires it to resources.

    This is the main interface for the developer.
    Used like:
        client = LumaClient()
        events = client.events.list()
    """

    def __init__(self, base_url: str, api_key:str, timeout: int = Requester.DEFAULT_TIMEOUT) -> None:
        self._requester = Requester(base_url=base_url, timeout=timeout, headers={"x-luma-api-key": api_key})
