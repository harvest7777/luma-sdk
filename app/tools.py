import os
from datetime import datetime
from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.tools import tool

from luma_sdk.luma_client import LumaClient
from luma_sdk.models.event import GuestInput

load_dotenv()

_luma = LumaClient(os.getenv("TEST_LUMA_API_KEY"))


def normalize(obj):
    """Convert SDK objects into JSON-serializable primitives."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    if hasattr(obj, "__dict__"):
        return normalize({k: v for k, v in vars(obj).items() if not k.startswith("_")})
    return str(obj)


@tool
def list_events(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sort_direction: Optional[Literal["asc", "desc", "asc nulls last", "desc nulls last"]] = None,
    pagination_cursor: Optional[str] = None,
) -> list[dict]:
    """List Luma calendar events with optional date filtering and sorting by start time.

    Args:
        after: ISO 8601 datetime string. Only return events starting after this time.
        before: ISO 8601 datetime string. Only return events starting before this time.
        sort_direction: Sort order by start_at. Use 'asc' for earliest-first, 'desc' for latest-first.
        pagination_cursor: Opaque cursor for fetching the next page of results.
    """
    events = list(_luma.list_events(
        after=datetime.fromisoformat(after) if after else None,
        before=datetime.fromisoformat(before) if before else None,
        sort_column="start_at",
        sort_direction=sort_direction,
        pagination_cursor=pagination_cursor,
    ))
    return [normalize(e) for e in events]


@tool
def get_event(event_id: str) -> dict:
    """Get full details for a specific Luma event by its ID.

    Args:
        event_id: The Luma event API ID (e.g. evt-abc123).
    """
    return normalize(_luma.get_event(event_id))

@tool
def register_for_event(event_id: str, email: str, name:str | None = None) -> dict:
    """Register a guest's email and name (optional) to an event ID.

    Args:
        event_id: The Luma event API ID (e.g. evt-abc123).
    """
    _luma.get_event(event_id).add_guests([GuestInput(email, name)])
    return normalize(_luma.get_event(event_id).get_guest(email))


