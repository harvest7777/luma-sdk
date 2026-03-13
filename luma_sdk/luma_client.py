from luma_sdk.models.event import Event
from luma_sdk.paginated_list import PaginatedList
from luma_sdk.requester import Requester


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

    _BASE_URL = "https://public-api.luma.com/v1"

    def __init__(self, api_key: str, timeout: int = Requester.DEFAULT_TIMEOUT) -> None:
        self._requester = Requester(base_url=self._BASE_URL, timeout=timeout, headers={"x-luma-api-key": api_key})

    # These all MUST be top level resources. We are following a RESTful ownership pattern
    def get_events(self, **filters) -> PaginatedList[Event]:
        return PaginatedList(self._requester, "/calendar/list-events", Event, params=filters, entry_key="event")

    def get_event(self, event_id: str) -> Event:
        data = self._requester.get("/event/get", parameters={"id": event_id})
        return Event(data["event"], self._requester)
