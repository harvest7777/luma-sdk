from __future__ import annotations

from typing import Generic, Iterator, TypeVar

from luma_sdk.domain_models.base import LumaModel
from luma_sdk.sdk_models.requester import HttpRequester

T = TypeVar("T", bound=LumaModel)


class PaginatedList(Generic[T]):
    def __init__(self, requester: HttpRequester, path: str, model_cls: type[T], params: dict | None = None, entry_key: str | None = None) -> None:
        self._requester = requester
        self._path = path
        self._model_cls = model_cls
        self._params = params or {}
        self._entry_key = entry_key

        self._elements: list[T] = []
        self._next_cursor: str | None = None
        self._has_more: bool = True

    def _fetch_next_page_and_update_state(self) -> None:
        params = {**self._params}
        if self._next_cursor:
            params["pagination_cursor"] = self._next_cursor

        data = self._requester.get(self._path, parameters=params)

        entries = [e[self._entry_key] if self._entry_key else e for e in data["entries"]]
        new_items = [self._model_cls(entry, self._requester) for entry in entries]
        self._elements.extend(new_items)
        self._has_more = data["has_more"]
        self._next_cursor = data.get("next_cursor")

    def __iter__(self) -> Iterator[T]:
        index = 0

        while True:
            if index < len(self._elements):
                yield self._elements[index]
                index += 1
            elif self._has_more:
                self._fetch_next_page_and_update_state()
            else:
                break
