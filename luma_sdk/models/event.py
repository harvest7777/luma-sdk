from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from luma_sdk.models.base import LumaModel
from luma_sdk.models.guest import Guest
from luma_sdk.paginated_list import PaginatedList
from luma_sdk.requester import HttpRequester
from luma_sdk.utils.datetime import parse_dt as _parse_dt


@dataclass
class GeoAddress:
    full_address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    google_maps_place_id: Optional[str]

    @classmethod
    def _from_dict(cls, data: dict) -> "GeoAddress":
        return cls(
            full_address=data.get("full_address"),
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            google_maps_place_id=data.get("google_maps_place_id"),
        )



class Event(LumaModel):
    def __init__(self, data: dict, requester: HttpRequester) -> None:
        super().__init__(data, requester)

        self.id: str = data["api_id"]
        self.calendar_id: str = data["calendar_api_id"]
        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description")
        self.description_md: Optional[str] = data.get("description_md")
        self.cover_url: Optional[str] = data.get("cover_url")
        self.url: Optional[str] = data.get("url")
        self.start_at: datetime = _parse_dt(data["start_at"])
        self.end_at: datetime = _parse_dt(data["end_at"])
        self.timezone: Optional[str] = data.get("timezone")
        self.visibility: Optional[str] = data.get("visibility")
        self.geo_address: Optional[GeoAddress] = (
            GeoAddress._from_dict(data["geo_address_json"])
            if data.get("geo_address_json")
            else None
        )

    def get_guest(self, guest_id: str) -> Guest:
        data = self._requester.get("/event/get-guest", parameters={"event_id": self.id, "id": guest_id})
        return Guest(data["guest"], self._requester)

    def get_guests(
        self,
        approval_status: Optional[Literal["approved", "session", "pending_approval", "invited", "declined", "waitlist"]] = None,
        sort_column: Optional[Literal["name", "email", "created_at", "registered_at", "checked_in_at"]] = None,
        sort_direction: Optional[Literal["asc", "desc", "asc nulls last", "desc nulls last"]] = None,
    ) -> PaginatedList[Guest]:
        params: dict = {"event_id": self.id}
        if approval_status is not None:
            params["approval_status"] = approval_status
        if sort_column is not None:
            params["sort_column"] = sort_column
        if sort_direction is not None:
            params["sort_direction"] = sort_direction
        return PaginatedList(
            self._requester,
            "/event/get-guests",
            Guest,
            params=params,
            entry_key="guest",
        )

    def __repr__(self) -> str:
        return f"<Event id={self.id!r} name={self.name!r}>"
