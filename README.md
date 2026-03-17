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
for event in client.list_events():
    print(event.name, event.url)

# fetch a guest on an event
guest = event.get_guest("gst-xyz789")
print(guest.user_email)
```

---

## Without the SDK

The same three examples using raw HTTP:

```python
import requests

headers = {"x-luma-api-key": "your_key_here", "Accept": "application/json"}

# fetch a single event
response = requests.get("https://public-api.luma.com/v1/event/get", headers=headers, params={"id": "evt-abc123"})
event = response.json()["event"]
print(event["name"], event["start_at"])

# iterate over all events (manual pagination)
cursor = None
while True:
    params = {"pagination_cursor": cursor} if cursor else {}
    response = requests.get("https://public-api.luma.com/v1/calendar/list-events", headers=headers, params=params)
    data = response.json()
    for entry in data["entries"]:
        print(entry["event"]["name"], entry["event"]["url"])
    if not data["has_more"]:
        break
    cursor = data["next_cursor"]

# fetch a guest on an event
response = requests.get("https://public-api.luma.com/v1/event/get-guest", headers=headers, params={"event_id": "evt-abc123", "id": "gst-xyz789"})
guest = response.json()["guest"]
print(guest["user"]["email"])
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

Contributors should not re-record cassettes. The cassettes are tied to a specific Luma calendar and API key held by the maintainers — re-recording against a different account will produce different data and break the assertions.

Maintainers only: set `LUMA_API_KEY` in a `.env` file and run with `--record-mode=all`. Cassettes scrub auth headers before saving and are safe to commit.

---

## `app/`

Example script using the SDK. Requires `LUMA_API_KEY` in `.env`.

```bash
python app/main.py
```
