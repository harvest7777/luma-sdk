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

## Usage

```python
from luma_sdk import LumaClient

client = LumaClient(api_key="your_key_here")

# fetch a single event
event = client.get_event("evt-abc123")
print(event.name, event.start_at)

# iterate over all events (pages automatically)
for event in client.get_events():
    print(event.name, event.url)

# fetch a guest on an event
guest = event.get_guest("gst-xyz789")
print(guest.user_email)
```

---

## `luma_sdk/`

The SDK package. Entry point is `LumaClient`.

---

## `tests/`

```
tests/
├── unit/          # pure logic, no HTTP
└── integration/   # real API shape, HTTP via VCR cassettes
```

Integration tests replay pre-recorded cassettes — **no network access or API key needed to run them.**

| Command | Behavior |
|---|---|
| `pytest tests/unit` | Logic tests, no network |
| `pytest tests/integration` | Replay cassettes, no network |
| `pytest tests/integration --record-mode=all` | Hit real API and re-record cassettes |

### Re-recording cassettes

Requires a valid `LUMA_API_KEY` in a `.env` file at the project root:

```
LUMA_API_KEY=your_key_here
```

Cassettes scrub auth headers before saving and are safe to commit.

---

## `app/`

Example script using the SDK. Requires `LUMA_API_KEY` in `.env`.

```bash
python app/main.py
```
