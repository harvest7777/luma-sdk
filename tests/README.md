# Tests

Uses [pytest-recording](https://github.com/kiwicom/pytest-recording) (VCR) to mock HTTP responses — no network required by default.

| Command | Behavior |
|---|---|
| `pytest` | Replay cassettes (no network) |
| `pytest --record-mode=all` | Real HTTP + re-record cassettes |
| `pytest --disable-recording` | Real HTTP, no recording |
