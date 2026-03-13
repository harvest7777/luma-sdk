from __future__ import annotations

from abc import ABC, abstractmethod

from luma_sdk.requester import HttpRequester


class LumaModel(ABC):
    """Base class for all Luma API resource models.

    Enforces a consistent constructor signature across every model so that
    PaginatedList can instantiate any model generically without knowing its
    concrete type.

    Subclasses must:
    - Call super().__init__(data, requester) as the first line of __init__
    - Implement __repr__ with the most useful identifying fields

    Do not assign self._requester manually in subclasses — the base handles it.
    """

    def __init__(self, data: dict, requester: HttpRequester) -> None:
        self._requester = requester

    @abstractmethod
    def __repr__(self) -> str: ...
