import os
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

from agent import agent as luma_agent

load_dotenv()

luma = Agent(
    name="luma",
    seed=os.getenv("LUMA_AGENT_SEED_PHRASE"),
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

protocol = Protocol(spec=chat_protocol_spec)


@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text

    now = datetime.now(timezone.utc).isoformat()
    response = "Unable to answer your question at this time."
    try:
        result = luma_agent.invoke({
            "messages": [{"role": "user", "content": f"{text} Today is {now}."}]
        })
        response = result["messages"][-1].content
    except Exception:
        ctx.logger.exception("Error running Luma agent")

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(tz=timezone.utc),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),
                EndSessionContent(type="end-session"),
            ],
        ),
    )


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


luma.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    luma.run()
