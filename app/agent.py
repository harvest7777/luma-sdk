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

agent = create_agent(llm, tools=[list_events, get_event, register_for_event])