# Pre-Push Review Plan

This document is for the AI agent to read and execute before any feature is pushed. Work through every section. Do not skip sections because the change seems small.

---

## 0. Pause and think

Before reviewing anything, re-read the change as a whole and ask:

- Is there a simpler way to do this that doesn't require a new abstraction?
- Does every new abstraction (base class, utility function, shared dataclass) have at least two concrete uses right now? If not, inline it and wait.
- Does anything feel unfamiliar or surprising in the diff? If yes, investigate before continuing.

If the answer to any of these changes your approach, stop and discuss with the user before proceeding.

---

## 1. Implementation guidelines

Cross-check against `luma_sdk/implementation_guide.md` line by line. Specifically:

- Every new top-level model extends `LumaModel` and calls `super().__init__(data, requester)` as its first line. `self._requester` is never assigned manually.
- Every embedded value object is a `@dataclass` with a `_from_dict` classmethod.
- If the same dataclass shape appears across two or more models, stop. Extract it before continuing — do not duplicate.
- All datetime fields use `parse_dt()` from `luma_sdk.utils.datetime`. No inline `fromisoformat` calls.
- Every model has a `__repr__` that includes its most identifying fields.
- Every new public model is added to `luma_sdk/__init__.py` and `__all__`.

---

## 2. Error handling and edge cases

This section requires the most scrutiny. Check every new code path.

### API shape
- Pull up the actual Luma API docs or cassette response for every field being parsed. Do not assume a field exists — verify it.
- Every field that can be absent in the API response must be accessed with `.get()` and typed as `Optional[X]`.
- Every field that is required must be accessed with `data["key"]` — not `.get()` — so a missing required field fails loudly and immediately.
- New models must not silently drop fields that appear in the API response and could be useful. If a field is in the API and we are not mapping it, leave a comment explaining why.

### Non-2xx responses
- Every new endpoint must have a test asserting the correct `ApiError` subclass is raised for relevant error conditions (403 → `ForbiddenError`, 404 → `NotFoundError`, etc.).
- Verify that no new code path lets a raw `requests` exception or HTTP error escape without being caught and re-raised as an `ApiError`.

### Null and optional fields
- Walk through every `Optional` field and mentally set it to `None`. Does the code downstream handle that without crashing?
- Check any code that chains off an optional (e.g. `guest.event_tickets[0].checked_in_at`) — these are crash sites if the list is empty or the field is `None`.

### Infinite loops and pagination
- Any new `PaginatedList` usage: confirm `has_more` and `next_cursor` are correctly threaded. A missing or always-truthy `has_more` causes an infinite loop.
- If a new endpoint has non-standard pagination, stop and verify the shape matches what `PaginatedList` expects before using it.

### Unexpected crashes
- Are there any bare `except:` or `except Exception:` blocks that swallow errors silently? Remove them.
- Are there any places where a `KeyError`, `TypeError`, or `AttributeError` could surface to the caller with no context? Add a clear failure before that happens.

---

## 3. Test coverage

### Integration tests (required for all HTTP verbs)
- Every new getter, updater, delete, or any other API call must have a corresponding `@pytest.mark.vcr` integration test.
- The cassette file must be committed alongside the test. If the cassette is missing, the test is incomplete.
- Each integration test must assert: return type (`isinstance`), at least one identifying field, and at least one non-trivial field.
- For sub-resources, the test must fetch the parent first, then the sub-resource — the cassette covers both requests.

### Error case tests
- Every error path identified in section 2 must have a test. Integration tests with VCR cassettes are preferred. If a cassette cannot cover a specific error shape, use a minimal `FakeRequester` stub — not a mock.

### Unit tests
- Only write unit tests for pure logic with no I/O: utility functions, pagination cursor threading, model parsing edge cases.
- Do not write unit tests that assert call wiring (e.g. "did `get()` get called with these args") — that is covered by integration tests.

---

## 4. Technical debt and anti-patterns

- Dependency direction: imports must flow downward. Models do not import from the client. Utils do not import from models. Draw the dependency chain if unsure.
- No new implicit contracts. If a function assumes a specific shape, enforce it with a type or validate at the boundary.
- No logic duplicated across files. If two places do the same thing, extract it — but only if it is genuinely the same thing and used in both places now.
- File size: if any model file exceeds ~200 lines, flag it and discuss extraction with the user before continuing.
- No debug artifacts: no `print()`, no commented-out code, no stray `TODO` unless intentional and discussed.

---

## 5. Public API surface

- Review `__all__` in `luma_sdk/__init__.py`. Everything listed there is a public contract. Adding to it is a commitment. Removing from it is a breaking change.
- Nothing internal (prefixed with `_`) should be accessible from the top-level package.
- If field names or types changed on any existing model, flag this as a breaking change and discuss with the user.

---

## 6. Commit hygiene

- Commits follow the order in `implementation_guide.md`: model → fetch method → integration tests → unit tests (if warranted).
- Each commit is one logical unit that could be reverted independently.
- Commit messages follow the existing repo convention (conventional commits, imperative, specific).
- No commit bundles unrelated changes.
