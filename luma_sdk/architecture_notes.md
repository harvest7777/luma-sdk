# Architecture Notes

## Open Issues

| Concern | Priority | Notes |
|---|---|---|
| `PaginatedList` implicit constructor contract | Medium | Every model must accept `(data, requester)` — not enforced. Fix before adding a second paginated resource. |
| Datetime parsing inconsistency | Low | `event.py` duplicates `parse_dt()` inline. Use the shared util. |
| `guest.py` God module risk | Watch | Extract ticket/order dataclasses if it grows past ~150 LOC. |

## Circular Imports

No runtime circular imports. `event.py` → `guest.py` cycle is broken via `TYPE_CHECKING` + lazy import in `get_guest()`. If a new model introduces a real cycle, rethink ownership before reachng for `TYPE_CHECKING` as a crutch.
