from core.models.event import Event
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

    # These all MUST be top level resources. We are following a RESTful ownership pattern
    def get_event(self, event_id):
        data = self._requester.get(f"/events/{event_id}")
        return Event(data, self._requester)
