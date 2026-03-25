import json
import os
import urllib.parse
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    Resource,
    ResourceContent,
    TextContent,
    chat_protocol_spec,
)

from agent import AGENT as luma_agent

load_dotenv()

luma = Agent(
    name="luma",
    seed=os.getenv("LUMA_AGENT_SEED_PHRASE"),
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

protocol = Protocol(spec=chat_protocol_spec)


def _extract_qr_url(messages) -> str | None:
    """Scan LangGraph tool messages for a check_in_qr_code value and return a qrserver URL."""
    for msg in messages:
        if not isinstance(msg, ToolMessage):
            continue
        try:
            data = json.loads(msg.content) if isinstance(msg.content, str) else msg.content
            if isinstance(data, dict) and "check_in_qr_code" in data:
                encoded = urllib.parse.quote(data["check_in_qr_code"])
                return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded}"
        except Exception:
            pass
    return None


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
    qr_url = None
    try:
        result = luma_agent.invoke({
            "messages": [{"role": "user", "content": f"{text} Today is {now}."}]
        })
        response = result["messages"][-1].content
        ctx.logger.info(response)
        qr_url = _extract_qr_url(result["messages"])
    except Exception:
        ctx.logger.exception("Error running Luma agent")

    content = [TextContent(type="text", text=response)]
    if qr_url:
        content.append(ResourceContent(
            resource_id=uuid4(),
            resource=Resource(
                uri=qr_url,
                metadata={"mime_type": "image/png", "role": "image"},
            ),
        ))
    content.append(EndSessionContent(type="end-session"))

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(tz=timezone.utc),
            msg_id=uuid4(),
            content=content,
        ),
    )


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


luma.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    luma.run()
