# Tests

```
tests/
  unit/        # logic only, no HTTP
  integration/ # real API calls, owns cassettes
```

Uses [pytest-recording](https://github.com/kiwicom/pytest-recording) (VCR) to mock HTTP in integration tests — no network required by default.

| Command                                           | Behavior                           |
| ------------------------------------------------- | ---------------------------------- |
| `pytest tests/unit`                               | Logic tests, no network            |
| `pytest tests/integration`                        | Replay cassettes (no network)      |
| `pytest tests/integration --record-mode=all`      | Real HTTP + re-record cassettes    |
| `pytest tests/integration --disable-recording`    | Real HTTP, no recording            |
