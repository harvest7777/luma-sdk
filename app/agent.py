import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents.middleware import SummarizationMiddleware

from tools import get_current_date, get_event, list_events, register_for_event

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=os.getenv("ASI_ONE_API_KEY"),
    model="asi1",
)

SYSTEM_PROMPT = """You are a helpful event assistant for attendees.

You can help users:
- Browse upcoming events and find details about specific events
- Register for events using their name and email

Guidelines:
- When listing events, summarize them clearly (name, date, location if available).
- Do not list or show past/outdated events unless the user explicitly asks about past events or specifies a time frame that includes the past. Default to upcoming events only.
- Before registering someone, confirm the event and their details (name + email) with them.
- Never register someone without their explicit confirmation.
- If the user asks about an event by name but you don't have its ID, use list_events to find it first.
- Keep responses concise and friendly.
"""

SUMMARY_PROMPT = """
Summarize the main thrust of this conversation. What have the human and assistant discussed so far? Focus on key facts and requests.

<messages>
Messages to summarize:
{messages}
</messages>
"""

AGENT = create_agent(
    llm,
    tools=[get_current_date, list_events, get_event, register_for_event],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=MemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model=llm,
            summary_prompt=SUMMARY_PROMPT,
            trigger=("tokens", 8192),
            keep=("tokens", 4096),
            # No additional trimming before summarization
            trim_tokens_to_summarize=None,
        ),
    ],
)