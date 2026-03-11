from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.requester import Requester


class _NotSetType:
    """
    Sentinel singleton. Distinguishes "not yet fetched" from None.

    Resource attributes start as NotSet. The first property access triggers
    a lazy GET if any attribute is still NotSet.
    """

    _instance: "_NotSetType | None" = None

    def __new__(cls) -> "_NotSetType":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "NotSet"

    def __bool__(self) -> bool:
        return False


NotSet = _NotSetType()


class Resource:
    """
    Base class for all API resource objects.

    Handles one thing: lazy loading. Attributes start as NotSet and are fetched
    on first access. HTTP verb methods (get, delete, list) belong on subclasses
    or on Client — not here — because not every resource supports every verb.

    Subclasses must implement:
      _init_attributes()  — set every attribute to NotSet
      _use_attributes()   — populate attributes from a raw API response dict
    """

    def __init__(
        self,
        requester: "Requester",
        url: str,
        attributes: dict | None = None,
    ) -> None:
        self._requester = requester
        self._url = url
        self._completed = False
        self._init_attributes()
        if attributes is not None:
            self._use_attributes(attributes)
            self._completed = True

    def _init_attributes(self) -> None:
        raise NotImplementedError

    def _use_attributes(self, attributes: dict) -> None:
        raise NotImplementedError

    def _complete_if_not_set(self, value: Any) -> None:
        if value is NotSet:
            self._complete_if_needed()

    def _complete_if_needed(self) -> None:
        if not self._completed:
            data = self._requester.request_json_and_check("GET", self._url)
            self._use_attributes(data)
            self._completed = True
