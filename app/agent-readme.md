# 📅 Luma Events Agent (Agent Chat Protocol)

A conversational agent that connects you to the Fetch.ai Luma calendar. Ask what's coming up, get details on a specific event, and register for one—all through natural chat. Powered by the Luma API and built for the Fetch.ai ecosystem.

---

## ✅ What this Agent Can Do

- **Browse upcoming events**
  - "What events are coming up?"
  - "Show me events this week"
  - "Are there any Fetch.ai events in April?"

- **Get event details**
  - "Tell me more about the hackathon"
  - "What time does the AI summit start?"
  - "Where is the next meetup?"

- **Register for an event**
  - "Register me for the Fetch.ai hackathon"
  - "Sign me up for that event"

- **Clear, formatted replies**
  - Event listings with name, date, and location
  - Full event details on request
  - Registration confirmation when you're ready to sign up

---

## ❌ What this Agent Will Not Do

- Access private or invite-only events not visible on the public Luma calendar
- Manage existing registrations (cancellations, transfers)
- Answer non-Luma questions (e.g., general trivia, weather)
- Support multiple Luma calendars in one conversation

---

## 🗣️ Example Prompts

| Prompt | Why it works |
| ------ | ------------ |
| "What's coming up on Luma?" | Browse the full upcoming event list |
| "Any events this weekend?" | Time-scoped event search |
| "Tell me about the AI hackathon" | Get details on a specific event |
| "What time does it start?" | Follow-up question on current event |
| "Register me for that one" | Kick off the registration flow |

---

## ℹ️ Tips for Best Results

- Ask "what's coming up" first to see the event list before drilling into details
- Be specific with event names when asking for details (e.g., "Fetch.ai hackathon" over "the hackathon")
- The agent knows today's date—time-relative questions like "this week" or "next month" work naturally
- Follow up in the same chat session; the agent holds context across turns

---

## 🎯 Typical Response Format

**Event listing:**

```
Here are the upcoming events:

1. Fetch.ai Hackathon — Sat Apr 12, 10:00 AM · San Francisco, CA
2. AI Summit 2025 — Thu Apr 17, 9:00 AM · Online
3. ...
```

**Event details:**

```
Fetch.ai Hackathon
📅 Saturday, April 12 · 10:00 AM – 6:00 PM PDT
📍 San Francisco, CA
🔗 lu.ma/...

Build on the Fetch.ai stack and compete for prizes. Open to all skill levels.
```

**Registration:**

```
You're registered for Fetch.ai Hackathon!
Check your email for a confirmation from Luma.
```

---

## 🤝 Use via ASI:One

Find this agent on ASI:One and start a chat:

```
What Luma events are happening this week?
```

```
Register me for the Fetch.ai hackathon
```

_(The agent's address is printed to the console when it starts, and published to the Fetch.ai agent directory.)_

---

## 🔌 How It Works (High-level)

1. Receives your message via the Agent Chat Protocol and acknowledges it
2. Injects the current date so time-relative questions ("this week", "upcoming") work correctly
3. Decides what to do—list events, fetch details, or start registration—via a LangChain ReAct agent
4. Calls the Luma API and formats the results into a readable reply
5. Sends the reply back to you in the same chat session

---

## 🛠️ Setup

1. **Create `app/.env`** with the following keys:

   ```
   LUMA_API_KEY=your-luma-api-key
   ASI_ONE_API_KEY=your-asi1-api-key
   LUMA_AGENT_SEED_PHRASE=your-agent-seed-phrase
   ```

2. **Install dependencies:**

   ```bash
   pip install -r app/docs/requirements-app.txt
   pip install -e .
   ```

3. **Run:**

   ```bash
   python app/fetchai_agent.py
   ```
