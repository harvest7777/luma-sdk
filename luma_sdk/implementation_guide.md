# Implementation Guide

This guide describes the standard workflow for adding new resources to the SDK. Follow these steps in order, committing at each stage.

---

## Step 1: Implement the model — commit

Add a new file at `luma_sdk/models/<resource>.py`.

**Rules:**
- Extend `LumaModel` (from `luma_sdk.models.base`) — this enforces the shared `(data, requester)` constructor contract and makes the class usable with `PaginatedList`.
- Call `super().__init__(data, requester)` as the first line of `__init__`. Do NOT assign `self._requester` manually.
- Use a plain class (not `@dataclass`) for the top-level model so it can hold a `_requester` for sub-resource methods later.
- Use `@dataclass` with a `_from_dict` classmethod for embedded value objects (e.g. `GeoAddress`, `EventTicket`, `RegistrationAnswer`). If this causes us duplication or pain, we must stop and look into refactoring first.
- Before creating new utility functions, check if they already exist in utils/
- Parse all datetime strings with `luma_sdk.utils.datetime.parse_dt`.
- Expose a `__repr__` with the most useful identifying fields.
- If we are facing circular imports, we must pause and re-articulate our architecture. Dependency flow should never be circular.
- Use if TYPE_CHECKING: for importing only types
- Add the new model to the __init__ __all__ export in luma_sdk

**Example structure:**

```python
# luma_sdk/models/widget.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from luma_sdk.models.base import LumaModel
from luma_sdk.requester import HttpRequester
from luma_sdk.utils.datetime import parse_dt as _parse_dt

@dataclass
class WidgetMeta:
    color: str
    weight: Optional[float]

    @classmethod
    def _from_dict(cls, data: dict) -> "WidgetMeta":
        return cls(color=data["color"], weight=data.get("weight"))

class Widget(LumaModel):
    def __init__(self, data: dict, requester: HttpRequester) -> None:
        super().__init__(data, requester)
        self.id: str = data["api_id"]
        self.name: str = data["name"]
        self.created_at: Optional[datetime] = _parse_dt(data.get("created_at"))
        self.meta: Optional[WidgetMeta] = (
            WidgetMeta._from_dict(data["meta"]) if data.get("meta") else None
        )

    def __repr__(self) -> str:
        return f"<Widget id={self.id!r} name={self.name!r}>"
```

Export the model from `luma_sdk/models/__init__.py` and `luma_sdk/__init__.py` if it should be part of the public API.

**Commit:** `feat: add Widget model`

---

## Step 2: Implement the fetch method — commit

Decide where the fetch method lives based on **ownership**:

| Resource ownership | Where to put it |
|---|---|
| Top-level resource (no parent) | `LumaClient` method |
| Sub-resource owned by a parent | Method on the parent model class |

**Top-level example** (`Event` is owned by the calendar/client):

```python
# luma_sdk/luma_client.py
def get_widget(self, widget_id: str) -> Widget:
    data = self._requester.get("/widget/get", parameters={"id": widget_id})
    return Widget(data["widget"], self._requester)

def get_widgets(self, **filters) -> PaginatedList[Widget]:
    return PaginatedList(self._requester, "/widget/list", Widget, params=filters, entry_key="widget")
```

**Sub-resource example** (`Guest` is owned by `Event`):

```python
# luma_sdk/models/event.py
def get_guest(self, guest_id: str) -> "Guest":
    from luma_sdk.models.guest import Guest  # inline import to avoid circular
    data = self._requester.get("/event/get-guest", parameters={"event_id": self.id, "id": guest_id})
    return Guest(data["guest"], self._requester)
```

**Commit:** `feat: add get_widget() to LumaClient` or `feat: add get_guest() to Event`

---

## Step 3: Write an integration test with VCR — commit

Add tests to `tests/integration/core/test_client.py`. Use `@pytest.mark.vcr` so the first run records a cassette and subsequent runs replay it.

**Rules:**
- Assert the return type with `isinstance`.
- Assert at least one identifying field (e.g. `id`) and one non-trivial field.
- For sub-resources, fetch the parent first, then the sub-resource — the VCR cassette covers both requests.
- For known error cases (e.g. forbidden ID), assert the correct exception is raised.

**Example:**

```python
@pytest.mark.vcr
def test_get_widget_returns_widget(luma_client):
    widget = luma_client.get_widget("wgt-abc123")
    assert isinstance(widget, Widget)
    assert widget.id == "wgt-abc123"
    assert isinstance(widget.name, str)
```

Run the tests once live (with a real API key) to generate the cassette, then verify the cassette was saved to `tests/cassettes/`. Subsequent CI runs use the recorded cassette only.

**Commit:** `test: add integration test for get_widget() with VCR cassette`

---

## Step 4: Write unit tests for pure logic — commit (only if needed)

Write unit tests for utility functions or state-transition logic that:
- Have no I/O or network dependency
- Do not require mocking collaborators just to assert call wiring

**Good candidates:**
- Utility functions like `parse_dt` in `luma_sdk/utils/`
- `PaginatedList` iteration and cursor-threading logic (use a minimal `FakeRequester` stub, not a mock)
- Model parsing edge cases (e.g. optional fields, nested objects, empty lists)

**Bad candidates (do not unit test these):**
- Whether `LumaClient.get_widget` calls `self._requester.get(...)` with the right args — that's wiring, covered by the integration test.
- Whether the model constructor sets `self.id = data["api_id"]` — that's trivially proven by the integration test.

**Example (pagination logic):**

```python
def test_cursor_threaded_to_next_fetch():
    captured_params = []

    class FakeRequester:
        call = 0
        def get(self, path, parameters=None):
            captured_params.append(parameters or {})
            if self.call == 0:
                self.call += 1
                return {"entries": [{"api_id": "a"}], "has_more": True, "next_cursor": "cur1"}
            return {"entries": [{"api_id": "b"}], "has_more": False, "next_cursor": None}

    list(PaginatedList(FakeRequester(), "/widgets", FakeModel))
    assert captured_params[1]["pagination_cursor"] == "cur1"
```

**Commit:** `test: add unit tests for Widget parsing edge cases`

---

## Summary

```
1. luma_sdk/models/<resource>.py       → model class + embedded dataclasses  → commit
2. luma_client.py or parent model      → fetch method(s)                     → commit
3. tests/integration/core/test_client  → @pytest.mark.vcr integration tests  → commit
4. tests/unit/core/                    → pure-logic unit tests (if warranted) → commit
```

Keep commits small and in this order. Do not bundle model + fetch + tests into one commit.
