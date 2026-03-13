# Architecture Notes

Observations on the current codebase structure — things that are working well and things worth rethinking before they become problems.

---

## Circular Imports

**Status: no runtime circular imports.**

`event.py` and `guest.py` have a potential cycle (`Event.get_guest` references `Guest`), but it is properly broken:

- `event.py` uses `if TYPE_CHECKING:` to import `Guest` for type annotations only
- `get_guest()` does a lazy inline import at call time: `from luma_sdk.models.guest import Guest`
- `guest.py` does not import `event.py` at all

No action needed here. If a new model introduces a real circular dependency, **stop and rethink ownership** before reaching for `TYPE_CHECKING` as a crutch.

---

## Things Worth Addressing

### 1. `PaginatedList` assumes a fixed model constructor signature

`PaginatedList` instantiates models like this:

```python
self._model_cls(entry, self._requester)
```

Every model must accept `(data: dict, requester: HttpRequester)` — but this contract is implicit and undocumented. Any future model that deviates breaks pagination with a confusing `TypeError`.

**Fix when:** you add a second paginated resource.
**How:** define a `ModelFactory` protocol or callable type alias, and thread that through `PaginatedList` instead of a bare `type[T]`.

---

### 2. `config.py` runs `load_dotenv()` at import time

```python
# config.py — runs on every import
load_dotenv()
```

Side effects at import time are a footgun. It runs in test contexts, CI, and library usage whether the caller wants it or not.

**Fix:** move `load_dotenv()` to application entry points (e.g. `app/main.py`), not the module level of `config.py`. `config.py` should just read env vars — let callers decide when to load the `.env` file.

---

### 3. Datetime parsing is inconsistent

`guest.py` uses the shared `parse_dt()` utility. `event.py` duplicates the same logic inline:

```python
# event.py — duplicated
datetime.fromisoformat(data["start_at"].replace("Z", "+00:00"))
```

**Fix:** replace the inline calls in `event.py` with `parse_dt()`. Low-effort, prevents drift if the parsing logic ever changes.

---

### 4. `guest.py` is a proto-God module

Currently defines five classes: `RegistrationAnswer`, `EventTicket`, `CouponInfo`, `EventTicketOrder`, and `Guest`. Fine at this size, but the Luma guest object is one of the richer API resources and will likely grow.

**Watch:** if `guest.py` crosses ~150–200 lines, extract the ticket/order dataclasses into a separate module (e.g. `models/ticket.py`) before it becomes hard to navigate.

---

## Dependency Direction (Healthy)

All imports flow downward. No surprises:

```
LumaClient
  ├── Requester
  ├── PaginatedList
  └── Event
        └── Guest (lazy)
              └── utils.datetime

PaginatedList[T]
  └── HttpRequester (Protocol)

Requester
  ├── requests
  └── exceptions

exceptions  ← leaf
utils/datetime  ← leaf
```

---

## Summary

| Concern | Priority | Notes |
|---|---|---|
| Circular imports | None | Handled correctly |
| `PaginatedList` implicit constructor contract | Medium | Fix before adding a second paginated resource |
| `config.py` import-time side effect | Medium | Move `load_dotenv()` to app entry points |
| Datetime parsing inconsistency | Low | Use `parse_dt()` in `event.py` |
| `guest.py` God module risk | Low/Watch | Revisit if it grows past ~150 LOC |
