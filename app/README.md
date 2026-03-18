# Luma Agent

Fetch.ai agent that answers questions about upcoming Luma events. Ask it what's coming up, get details on a specific event, or ask it to register you for one.

---

## Architecture

**One entry point.** All chat traffic flows through `fetchai_agent.py` → `agent.invoke(message)` → reply string. The uAgents layer handles the chat protocol; the LangChain layer handles tool-calling against the Luma API.

| Layer | Purpose |
|-------|---------|
| **fetchai_agent.py** | uAgents chat protocol adapter. Receives `ChatMessage`, sends `ChatAcknowledgement`, runs the agent, replies with `ChatMessage`. |
| **agent.py** | LangChain ReAct agent (LangGraph). Decides which tools to call based on the user's question. Pointed at ASI1. |
| **tools.py** | Luma API tools: `list_events`, `get_event`. Each tool normalizes SDK objects into plain dicts the LLM can reason over. |

**Flow:** User message via ASI:One → `handle_message` → inject current datetime → `agent.invoke()` → tool calls against Luma API → final reply → `ChatMessage` back to user.

---

## Project layout

```
app/
  fetchai_agent.py   # uAgents entry point (chat protocol)
  agent.py           # LangChain ReAct agent + LLM config
  tools.py           # Luma API tools (@tool decorated)
  docs/
    requirements-app.txt
luma_sdk/            # Luma API client + models (used by tools.py)
```

---

## Capabilities

- **Find upcoming events** — ask "what Luma events are coming up?" and the agent queries the Luma calendar, filters by date, and summarizes what it finds.
- **Get event details** — ask about a specific event by name or ID to get the full description, location, and timing.
- **Register for an event** — coming soon.

---

## Setup

1. **Copy env:** create `app/.env` with the following keys:

   ```
   LUMA_API_KEY=your-luma-api-key
   ASI_ONE_API_KEY=your-asi1-api-key
   LUMA_AGENT_SEED_PHRASE=your-agent-seed-phrase
   ```

2. **Install dependencies:**

   ```bash
   pip install -r app/docs/requirements-app.txt
   pip install -e .   # installs luma_sdk from the repo root
   ```

---

## Usage

**Run the agent:**

```bash
python app/fetchai_agent.py
```

The agent registers on the Fetch.ai network and starts listening for chat messages. Find it on [ASI:One](https://asi1.ai) by its published agent address, then start chatting:

> "What Luma events are happening this week?"

> "Tell me more about the Fetch.ai hackathon."

---

## Tests

```bash
pytest tests/
```

Integration tests use VCR cassettes — no live API calls needed.
