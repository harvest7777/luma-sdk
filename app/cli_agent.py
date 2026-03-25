import uuid
from app.agent import AGENT

print("=" * 40)
print("  Luma Agent CLI")
print("  Type your request. Ctrl+C to quit.")
print("=" * 40)
print()

thread_id = str(uuid.uuid4())

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
        print("\nGoodbye!")
        break