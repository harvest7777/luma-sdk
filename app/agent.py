import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import get_event, list_events, register_for_event

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
- Before registering someone, confirm the event and their details (name + email) with them.
- Never register someone without their explicit confirmation.
- If the user asks about an event by name but you don't have its ID, use list_events to find it first.
- Keep responses concise and friendly.
"""

AGENT = create_agent(llm, tools=[list_events, get_event, register_for_event], system_prompt=SYSTEM_PROMPT)