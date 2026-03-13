# luma-sdk

A Python SDK for the [Luma](https://lu.ma) public API, modeled after PyGitHub's architecture.

## Project Structure

```
luma-sdk/
├── luma_sdk/       # the SDK package
├── tests/          # unit and integration tests
└── app/            # example application using the SDK
```

---

## `luma_sdk/`

The SDK itself. The entry point for callers is `LumaClient`.

### Architecture

```
LumaClient
  ├── Requester          # owns the HTTP session, auth headers, error mapping
  ├── PaginatedList[T]   # lazy iterator that pages through API responses
  └── models/
        ├── LumaModel    # abstract base: accepts (data, requester), requires __repr__
        ├── Event        # top-level resource
        └── Guest        # sub-resource accessed through Event
```

**Dependency direction is strictly top-down.** `LumaClient` depends on `Requester` and models. Models depend on `Requester` (via the `HttpRequester` protocol). Nothing lower in the tree imports from above it.

### Key design decisions

**`Requester` is injected, not global.** `LumaClient` constructs a `Requester` with the API key baked into the session headers. Models receive it at construction time and use it for sub-resource fetches (e.g. `event.get_guest(...)`). This keeps HTTP concerns out of models and makes the dependency explicit.

**`HttpRequester` is a Protocol.** Models type-hint against `HttpRequester`, not the concrete `Requester`. This keeps models decoupled from the HTTP implementation.

**`PaginatedList` is a lazy iterator.** It fetches pages on demand as you iterate — no eagerly loading all results upfront. It follows cursor-based pagination using `next_cursor` from the API response.

**Errors are typed.** `Requester` maps HTTP status codes to specific exception classes (`NotFoundError`, `ForbiddenError`, `ClientError`, `ServerError`, `RequestTimeoutError`), all inheriting from `ApiError`.

---

## `tests/`

```
tests/
├── unit/          # pure logic, no HTTP
└── integration/   # real API shape, HTTP via VCR cassettes
```

### Unit tests

Test logic in isolation — pagination behavior, URL construction, error mapping, datetime parsing. No network, no mocks of collaborators.

### Integration tests

Test the full stack against real API responses. HTTP is intercepted by [VCR.py](https://vcrpy.readthedocs.io) via [pytest-recording](https://github.com/kiwicom/pytest-recording). Pre-recorded cassettes are committed to the repo, so **no network access or API key is needed to run them.**

| Command | Behavior |
|---|---|
| `pytest tests/unit` | Logic tests, no network |
| `pytest tests/integration` | Replay cassettes, no network |
| `pytest tests/integration --record-mode=all` | Hit real API and re-record cassettes |
| `pytest tests/integration --disable-recording` | Hit real API, no recording |

### Re-recording cassettes

Cassettes can only be re-recorded by someone with a valid `LUMA_API_KEY`. Set it in a `.env` file at the project root:

```
LUMA_API_KEY=your_key_here
```

Cassettes scrub sensitive data before saving — auth headers in both requests and responses are replaced with a redacted placeholder. Cassettes are safe to commit.

---

## `app/`

An example script that uses the SDK. Run it with a valid `LUMA_API_KEY` in your `.env`:

```bash
python app/main.py
```
