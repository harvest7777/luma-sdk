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

    Subclasses must implement:
      _init_attributes()  — set every attribute to NotSet
      _use_attributes()   — populate attributes from a raw API response dict

    To add a resource:
      1. Subclass Resource
      2. Set attributes to NotSet in _init_attributes()
      3. Populate from the response dict in _use_attributes()
      4. Expose each attribute as a @property that calls _complete_if_not_set()
      5. Add child-resource methods (e.g. get_comments()) that call self._requester
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
