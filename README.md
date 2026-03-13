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

## Without the SDK

The same script without the SDK, using raw HTTP calls:

```python
import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

headers = {"x-luma-api-key": os.getenv("LUMA_API_KEY"), "Accept": "application/json"}
now = datetime.now(timezone.utc)
upcoming = []

cursor = None
while True:
    params = {"pagination_cursor": cursor} if cursor else {}
    response = requests.get("https://public-api.luma.com/v1/calendar/list-events", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    for entry in data["entries"]:
        event = entry["event"]
        start_at = datetime.fromisoformat(event["start_at"].replace("Z", "+00:00"))
        if start_at >= now:
            upcoming.append(event)

    if not data["has_more"]:
        break
    cursor = data["next_cursor"]

print(f"Fetch.ai upcoming events ({len(upcoming)} total):\n")
for event in upcoming:
    start_at = datetime.fromisoformat(event["start_at"].replace("Z", "+00:00"))
    print(f"  {start_at.strftime('%Y-%m-%d')}  {event['name']}")
    print(f"           {event['url']}")
    print()
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
