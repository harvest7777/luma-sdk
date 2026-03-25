from app.agent import agent

print("=" * 40)
print("  Luma Agent CLI")
print("  Type your request. Ctrl+C to quit.")
print("=" * 40)
print()

while True:
    try:
        user_message = input("You: ")
        res = agent.invoke({
            "messages": [{"role": "user", "content": f"{user_message}."}]
        })
        ai_message = res["messages"][-1].content
        print(f"\nAgent: {ai_message}\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break