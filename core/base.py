from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.requester import Requester


class _NotSetType:
    """
    Sentinel singleton. Distinguishes "attribute not yet fetched" from None.

    Every resource attribute starts as NotSet. The first property access checks
    for NotSet and triggers a lazy GET before returning the value. This lets
    resources be created cheaply from partial data (e.g. list responses) and
    only fetch their full representation on demand.
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


class GithubObject:
    """
    Base class for all SDK resource objects. Mirrors PyGithub's GithubObject.

    Subclasses must implement:
      _initAttributes()   — set every instance attribute to NotSet
      _useAttributes()    — populate attributes from a raw API response dict

    Lifecycle:
      1. __init__ stores the requester + URL, calls _initAttributes()
      2. If `attributes` is passed (fast path from list responses), _useAttributes()
         is called immediately and no network call is needed
      3. On first @property access of a NotSet attr, _completeIfNotSet() fires
         _completeIfNeeded() which GETs self._url and calls _useAttributes()
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
        self._initAttributes()
        if attributes is not None:
            self._useAttributes(attributes)
            self._completed = True

    def _initAttributes(self) -> None:
        raise NotImplementedError

    def _useAttributes(self, attributes: dict) -> None:
        raise NotImplementedError

    def _completeIfNotSet(self, value: Any) -> None:
        if value is NotSet:
            self._completeIfNeeded()

    def _completeIfNeeded(self) -> None:
        if not self._completed:
            data = self._requester.request_json_and_check("GET", self._url)
            self._useAttributes(data)
            self._completed = True
