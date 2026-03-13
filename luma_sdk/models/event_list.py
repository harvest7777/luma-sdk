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
    def __init__(self, requester, path, params):
        raise NotImplementedError
