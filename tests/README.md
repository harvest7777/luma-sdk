# Tests

Uses [pytest-recording](https://github.com/kiwicom/pytest-recording) (VCR) to mock HTTP responses — no network required by default.

| Command                      | Behavior                           |
| ---------------------------- | ---------------------------------- |
| `pytest`                     | Replay cassettes (no network)      |
| `pytest --record-mode=all`   | Real HTTP + re-record interactions |
| `pytest --disable-recording` | Real HTTP, no recording            |

## Regenerating Cassettes

To fully regenerate cassette files, delete them first:

```bash
rm -rf tests/cassettes
pytest --record-mode=all
```

This guarantees fresh recordings.
