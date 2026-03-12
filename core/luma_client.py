from core.requester import Requester


class LumaClient:
    """
    Base entry point for an SDK. Owns the Requester and wires it to resources.

    This is the main interface for the developer.
    Used like:
        client = LumaClient(api_key=....)
        client.get_events()          # returns PaginatedList[Event]
        client.get_event(event_id)   # returns Event
        event.get_tickets()          # returns PaginatedList[Ticket]
    """

    _BASE_URL = "https://api.lu.ma/public/v1"

    def __init__(self, api_key: str, timeout: int = Requester.DEFAULT_TIMEOUT) -> None:
        self._requester = Requester(base_url=self._BASE_URL, timeout=timeout, headers={"x-luma-api-key": api_key})
