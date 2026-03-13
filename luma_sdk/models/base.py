from __future__ import annotations

from abc import ABC, abstractmethod

from luma_sdk.requester import HttpRequester


class LumaModel(ABC):
    def __init__(self, data: dict, requester: HttpRequester) -> None:
        self._requester = requester

    @abstractmethod
    def __repr__(self) -> str: ...
