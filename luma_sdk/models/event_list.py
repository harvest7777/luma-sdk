class EventList:
    """
    This is only responsible for abstracting pagination.
    How to use:
    def list_events(self, **filters):
        return PaginatedList(
            requester=self._requester,
            path="/calendar/list-events",
            params=filters,
            model_cls=Event
        )
    """
    def __init__(self, requester, params=None):
        self._requester = requester
        self._params = params or {}

        self._elements = []
        self._next_cursor = None
        self._has_more = True

    def _fetch_next_page_and_update_states(self):
        pass

    def __iter__(self):
        index = 0

        while True:
            if index < len(self._elements):
                yield self._elements[index]
                index += 1

            elif self._has_more:
                self._fetch_next_page_and_update_states()
            else:
                break