import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools import get_event, list_events

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.asi1.ai/v1",
    api_key=os.getenv("ASI_ONE_API_KEY"),
    model="asi1",
)

agent = create_agent(llm, tools=[list_events, get_event])

if __name__ == "__main__":
    now = datetime.now(timezone.utc).isoformat()
    result = agent.invoke({
        "messages": [{"role": "user", "content": f"What are the next 5 upcoming Luma events? Today is {now}."}]
    })
    print(result["messages"][-1].content)
