import argparse
import uuid
from app.agent import AGENT

parser = argparse.ArgumentParser()
parser.add_argument("--resume", metavar="THREAD_ID", help="Resume a previous session")
args = parser.parse_args()

thread_id = args.resume or str(uuid.uuid4())

print("=" * 40)
print("  Luma Agent CLI")
print("  Type your request. Ctrl+C to quit.")
print("=" * 40)
print()

while True:
    try:
        user_message = input("You: ")
        res = AGENT.invoke(
            {"messages": [{"role": "user", "content": f"{user_message}."}]},
            config={"configurable": {"thread_id": thread_id}},
        )
        ai_message = res["messages"][-1].content
        print(f"\nAgent: {ai_message}\n")
    except KeyboardInterrupt:
        print(f"\nGoodbye! Resume this session with: --resume {thread_id}")
        break