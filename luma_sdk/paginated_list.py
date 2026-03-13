from __future__ import annotations

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class PaginatedList(Generic[T]):
    def __init__(self, requester, path: str, model_cls: type[T], params: dict | None = None) -> None:
        self._requester = requester
        self._path = path
        self._model_cls = model_cls
        self._params = params or {}

        self._elements: list[T] = []
        self._next_cursor: str | None = None
        self._has_more: bool = True

    def _fetch_next_page_and_update_state(self) -> None:
        params = {**self._params}
        if self._next_cursor:
            params["pagination_cursor"] = self._next_cursor

        data = self._requester.get(self._path, parameters=params)

        new_items = [self._model_cls(entry, self._requester) for entry in data["entries"]]
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
