from __future__ import annotations

from abc import ABC, abstractmethod

from luma_sdk.sdk_models.requester import HttpRequester


class LumaModel(ABC):
    """Base class for all Luma API resource domain_models.

    Guarantees that every model can be constructed from a raw API response dict
    and an HTTP requester, and that it has a human-readable representation.
    """

    def __init__(self, data: dict, requester: HttpRequester) -> None:
        self._requester = requester

    @abstractmethod
    def __repr__(self) -> str: ...
