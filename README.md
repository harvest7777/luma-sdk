# SDK Scaffold

A minimal Python SDK scaffold with clean separation of concerns, mirroring [PyGithub](https://github.com/PyGithub/PyGithub)'s architecture. Use this as a starting point for wrapping any REST API.

## Architecture

```
core/
├── client.py       # Entry point — owns the Requester, exposes resource methods
├── requester.py    # HTTP transport — the only layer that touches the network
├── base.py         # Resource base class with lazy loading via NotSet sentinel
├── exceptions.py   # Typed exception hierarchy mapped from HTTP status codes
└── resources/      # One file per API resource (add yours here)
```

Each layer has one job and no knowledge of the others above it.

## Adding a resource

**1. Subclass `Resource` in `core/resources/`:**

```python
# core/resources/post.py
from core.base import Resource, NotSet

class Post(Resource):
    def _init_attributes(self):
        self._id = NotSet
        self._title = NotSet

    def _use_attributes(self, data):
        if "id" in data:
            self._id = int(data["id"])
        if "title" in data:
            self._title = str(data["title"])

    @property
    def id(self) -> int:
        self._complete_if_not_set(self._id)
        return self._id

    @property
    def title(self) -> str:
        self._complete_if_not_set(self._title)
        return self._title

    def get_comments(self) -> list:
        raw = self._requester.request_json_and_check("GET", f"{self._url}/comments")
        return [Comment(self._requester, f"/comments/{c['id']}", attributes=c) for c in raw]
```

**2. Expose it from `Client`:**

```python
# core/client.py
from core.resources.post import Post

class Client:
    def get_post(self, post_id: int) -> Post:
        return Post(self._requester, f"/posts/{post_id}")
```

**3. Use it:**

```python
from core.client import Client

client = Client(base_url="https://api.example.com")
post = client.get_post(1)   # no HTTP call yet
print(post.title)           # lazy GET /posts/1 fires here
comments = post.get_comments()
```

## Lazy loading

Resources are shells until first attribute access. `get_post(1)` just constructs a `Post` object with a URL — no network call. The first time you touch `.title`, `.id`, etc., the `GET /posts/1` fires and all attributes populate at once.

If you already have the response data (e.g., from a list endpoint), pass it as `attributes=` to skip the fetch entirely:

```python
Post(requester, "/posts/1", attributes={"id": 1, "title": "..."})
```

## Exceptions

| Exception | HTTP status |
|---|---|
| `NotFoundError` | 404 |
| `ClientError` | 4xx (non-404) |
| `ServerError` | 5xx |

All inherit from `ApiError`, which exposes `.status` and `.data`.

## Installation

```bash
pip install -e ".[dev]"
```

Requires Python 3.11+.
