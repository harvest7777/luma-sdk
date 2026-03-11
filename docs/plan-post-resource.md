# Plan: Post resource (TDD)

Each step follows the red → green → commit cycle. Write the test first,
confirm it fails for the right reason, then write the minimum code to make
it pass.

---

## Step 1 — Comment attributes (leaf resource, no deps)

**Why first:** `Post.get_comments()` returns `Comment` objects, so `Comment`
must exist before `Post` can be fully tested.

### 1a. Write the failing test

`tests/test_comment.py`

```python
def test_comment_attributes():
    requester = ...  # see note on mocking below
    comment = Comment(requester, "/comments/1", attributes={
        "id": 1, "postId": 1,
        "name": "a name", "email": "a@b.com", "body": "some body",
    })
    assert comment.id == 1
    assert comment.post_id == 1
    assert comment.email == "a@b.com"
```

> **Note on mocking the requester:** because `attributes=` is passed,
> `_complete_if_needed()` never fires. The requester is never called.
> Pass `None` or a `MagicMock` — it won't matter for this test.

Run: `pytest tests/test_comment.py` → **ImportError** (no `Comment` yet). That's the expected red.

### 1b. Make it green

Create `core/resources/comment.py` — subclass `Resource`, implement
`_init_attributes` and `_use_attributes`, add lazy `@property` for each
attribute. No child-resource methods.

Run: `pytest tests/test_comment.py` → **green**.

### 1c. Commit

```
feat: add Comment resource
```

---

## Step 2 — Post attributes (lazy fetch)

### 2a. Write the failing test

`tests/test_post.py`

```python
@pytest.mark.vcr
def test_post_attributes():
    client = Client(base_url="https://jsonplaceholder.typicode.com")
    post = client.get_post(1)
    assert post.id == 1
    assert post.user_id == 1
    assert post.title == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
```

Run: `pytest tests/test_post.py` → **ImportError** or **AttributeError** (no
`Post`, no `client.get_post`). That's the expected red.

### 2b. Make it green

1. Create `core/resources/post.py` — `_init_attributes`, `_use_attributes`
   for `id`, `user_id`, `title`, `body`. Lazy `@property` for each.
2. Add `get_post(post_id)` to `Client`.
3. Record the cassette:
   ```
   pytest tests/test_post.py::test_post_attributes --record-mode=once
   ```

Run: `pytest tests/test_post.py::test_post_attributes` → **green**.

### 2c. Commit

```
feat: add Post resource with lazy-loaded attributes
```

---

## Step 3 — Post attributes skip the fetch when pre-filled

This test proves the lazy-load fast path works: if `attributes=` is given,
no HTTP call should fire.

### 3a. Write the failing test

```python
from unittest.mock import MagicMock

def test_post_attributes_no_fetch_when_pre_filled():
    mock_requester = MagicMock()
    post = Post(mock_requester, "/posts/1", attributes={
        "id": 1, "userId": 1,
        "title": "a title", "body": "a body",
    })
    assert post.title == "a title"
    mock_requester.request_json_and_check.assert_not_called()
```

Run: `pytest tests/test_post.py::test_post_attributes_no_fetch_when_pre_filled`
→ **red** (no `Post` import yet if step 2 isn't done, or green if it is —
in which case this is a safety net test added alongside step 2).

> Add this test in the same commit as step 2 if `Post` already exists.
> If added before, it drives the `attributes=` fast path in `Resource.__init__`.

### 3b. No new code needed

`Resource.__init__` already handles this. The test just pins the behavior.

Run → **green**.

---

## Step 4 — Post.get_comments()

### 4a. Write the failing test

```python
@pytest.mark.vcr
def test_post_get_comments():
    client = Client(base_url="https://jsonplaceholder.typicode.com")
    post = client.get_post(1)
    comments = post.get_comments()
    assert len(comments) == 5
    assert comments[0].email == "Eliseo@gardner.biz"
    assert isinstance(comments[0], Comment)
```

Run: `pytest tests/test_post.py::test_post_get_comments` → **AttributeError**
(`Post` has no `get_comments`). That's the expected red.

### 4b. Make it green

Add `get_comments()` to `Post`:

```python
def get_comments(self) -> list[Comment]:
    raw = self._requester.request_json_and_check("GET", f"{self._url}/comments")
    return [
        Comment(self._requester, f"/comments/{c['id']}", attributes=c)
        for c in raw
    ]
```

Record the cassette:
```
pytest tests/test_post.py::test_post_get_comments --record-mode=once
```

Run: `pytest tests/test_post.py::test_post_get_comments` → **green**.

### 4c. Commit

```
feat: add Post.get_comments()
```

---

## Step 5 — Full suite stays green

```
pytest
```

All tests pass. No regressions.

### 5a. Commit (if any fixups needed)

```
fix: <whatever broke>
```

---

## File checklist

| File | Action |
|---|---|
| `core/resources/comment.py` | Create |
| `core/resources/post.py` | Create |
| `core/client.py` | Add `get_post()` |
| `tests/test_comment.py` | Create |
| `tests/test_post.py` | Create |
| `tests/cassettes/test_post/test_post_attributes.yaml` | Auto-recorded |
| `tests/cassettes/test_post/test_post_get_comments.yaml` | Auto-recorded |

---

## Red/green rules for this project

- A test that fails with **ImportError** or **AttributeError** counts as red —
  the interface doesn't exist yet.
- Only write enough code to turn the current red test green. Don't implement
  `get_comments()` while working on step 2.
- Cassettes are recorded once (`--record-mode=once`) as part of making a test
  green. They're committed with the same commit as the code that uses them.
- `mock_requester` (via `MagicMock`) is used only when testing behavior that
  must not make a network call. For everything else, use a real cassette.
