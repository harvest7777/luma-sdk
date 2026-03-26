import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.tools import tool
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential, wait_random

from luma_sdk.exceptions import (
    ApiError,
    ClientError,
    EventNotFoundError,
    ForbiddenError,
    GuestNotFoundError,
    TransientError,
)
from luma_sdk.luma_client import LumaClient
from luma_sdk.models.event import GuestInput

load_dotenv()

_luma = LumaClient(os.getenv("TEST_LUMA_API_KEY"))

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class ToolError:
    message: str
    type: str

    def to_dict(self) -> dict:
        return {"error": self.message, "type": self.type}


_retry_transient_call = retry(
    retry=retry_if_exception_type(TransientError),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8) + wait_random(0, 0.5),
    reraise=True,
)


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


def _tool_error_from_exc(exc: Exception) -> ToolError:
    if isinstance(exc, ForbiddenError):
        return ToolError("Access denied. Check your Luma API key.", "forbidden")
    if isinstance(exc, TransientError):
        return ToolError(f"Request failed: {exc}, retrying", "transient_error")
    if isinstance(exc, (ClientError, ApiError)):
        return ToolError(f"Luma API error: {exc}", "api_error")
    return ToolError(f"Unexpected error: {exc}", "api_error")


@tool
def get_current_date() -> str:
    """Returns the current UTC date and time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


@tool
def list_events(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sort_direction: Optional[Literal["asc", "desc", "asc nulls last", "desc nulls last"]] = None,
    pagination_cursor: Optional[str] = None,
) -> list[dict] | dict:
    """List Luma calendar events with optional date filtering and sorting by start time.

    Args:
        after: ISO 8601 datetime string. Only return events starting after this time.
        before: ISO 8601 datetime string. Only return events starting before this time.
        sort_direction: Sort order by start_at. Use 'asc' for earliest-first, 'desc' for latest-first.
        pagination_cursor: Opaque cursor for fetching the next page of results.
    """
    try:
        after_dt = datetime.fromisoformat(after) if after else None
        before_dt = datetime.fromisoformat(before) if before else None
    except ValueError as e:
        return ToolError(f"Invalid date format: {e}. Use ISO 8601 (e.g. 2025-01-01T00:00:00).", "input_error").to_dict()

    try:
        events = _retry_transient_call(lambda: list(_luma.list_events(
            after=after_dt,
            before=before_dt,
            sort_column="start_at",
            sort_direction=sort_direction,
            pagination_cursor=pagination_cursor,
        )))
        return [normalize(e) for e in events]
    except Exception as exc:
        return _tool_error_from_exc(exc).to_dict()


@tool
def get_event(event_id: str) -> dict:
    """Get full details for a specific Luma event by its ID.

    Args:
        event_id: The Luma event API ID (e.g. evt-abc123).
    """
    if not event_id or not event_id.strip():
        return ToolError("event_id is required.", "input_error").to_dict()

    try:
        return normalize(_retry_transient_call(lambda: _luma.get_event(event_id)))
    except EventNotFoundError:
        return ToolError(f"Event '{event_id}' not found.", "not_found").to_dict()
    except Exception as exc:
        return _tool_error_from_exc(exc).to_dict()


@tool
def register_for_event(event_id: str, email: str, name: str | None = None) -> dict:
    """Register a guest's email and name (optional) to an event ID.

    Args:
        event_id: The Luma event API ID (e.g. evt-abc123).
        email: The guest's email address.
        name: The guest's name (optional).
    """
    if not event_id or not event_id.strip():
        return ToolError("event_id is required.", "input_error").to_dict()
    if not email or not _EMAIL_RE.match(email):
        return ToolError(f"Invalid email address: {email!r}.", "input_error").to_dict()

    try:
        event = _retry_transient_call(lambda: _luma.get_event(event_id))
    except EventNotFoundError:
        return ToolError(f"Event '{event_id}' not found.", "not_found").to_dict()
    except Exception as exc:
        return _tool_error_from_exc(exc).to_dict()

    try:
        _retry_transient_call(lambda: event.add_guests([GuestInput(email, name)]))
    except ForbiddenError:
        return ToolError("Not allowed to add guests to this event.", "forbidden").to_dict()
    except Exception as exc:
        return _tool_error_from_exc(exc).to_dict()

    try:
        return normalize(_retry_transient_call(lambda: event.get_guest(email)))
    except GuestNotFoundError:
        return ToolError(f"Guest '{email}' was not found after registration.", "not_found").to_dict()
    except Exception as exc:
        return _tool_error_from_exc(exc).to_dict()
