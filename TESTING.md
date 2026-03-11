# Testing

Tests run fully offline by default using pre-recorded HTTP cassettes. No API key or network access required.

## Running tests

```bash
pytest
```

## How cassettes work

Each test decorated with `@pytest.mark.vcr` has a corresponding YAML file in `tests/cassettes/` that contains the recorded HTTP request and response. When the test runs, `vcrpy` intercepts the network call and replays the saved response instead of hitting the real API.

Cassettes are stored at:
```
tests/cassettes/{test_module}/{test_name}.yaml
```

They are committed to git, so API response shapes are version-controlled and diffs are visible in code review.

## Writing a test with a cassette

```python
@pytest.mark.vcr
def test_get_post(requester):
    data = requester.request_json_and_check("GET", "/posts/1")
    assert data["id"] == 1
```

On the first run with `--record-mode=once`, vcrpy hits the real API and writes the cassette. Every subsequent run replays it.

## Recording and regenerating cassettes

| Command | Behavior |
|---|---|
| `pytest` | Replay only. Fails if a cassette is missing. |
| `pytest --record-mode=once` | Record missing cassettes, replay existing ones. |
| `pytest --record-mode=all` | Re-record every cassette from the live API. |
| `pytest --record-mode=new_episodes` | Add new interactions to existing cassettes. |

Use `--record-mode=all` when the upstream API changes shape. The cassette diff will show exactly what changed in the response.

## Cassette format

Cassettes are plain YAML. Each file contains one or more request/response pairs:

```yaml
interactions:
- request:
    method: GET
    uri: https://api.example.com/posts/1
    body: null
    headers:
      Accept: [application/json]
  response:
    status:
      code: 200
      message: OK
    headers:
      Content-Type: [application/json; charset=utf-8]
    body:
      string: '{"id": 1, "title": "..."}'
version: 1
```

You can edit cassettes by hand to test edge cases (e.g., malformed responses, specific error payloads) without needing the real API to reproduce them.

## Testing error handling

Write the cassette with the desired error status, then assert the exception:

```python
@pytest.mark.vcr
def test_raises_not_found_on_404(requester):
    with pytest.raises(NotFoundError) as exc_info:
        requester.request_json_and_check("GET", "/posts/9999")
    assert exc_info.value.status == 404
```

The cassette for this test returns a 404 — no need to find a real endpoint that 404s.

## Configuration

`vcr_config` and `vcr_cassette_dir` are defined in `tests/conftest.py`. The default `record_mode` is `none`, which prevents any accidental live API calls in CI.

Authorization headers are automatically stripped from recorded cassettes via `filter_headers`.
