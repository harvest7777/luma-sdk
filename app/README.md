# Luma Agent

An agent that answers questions about Luma events and handles registrations. Supports two runtimes: a CLI for local use and a Fetch.ai agent for the ASI:One ecosystem.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- A `.env` file in this directory:

```
LUMA_API_KEY=...
ASI_ONE_API_KEY=...
LUMA_AGENT_SEED_PHRASE=...
```

## Usage

**CLI**

```bash
uv run cli_agent.py
uv run cli_agent.py --resume <thread-id>   # resume a previous session
```

**Fetch.ai agent**

```bash
uv run fetchai_agent.py
```

The agent's address is printed to the console on startup. Find it on ASI:One to start a chat.
