from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from luma_sdk.requester import HttpRequester


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



class Event:
    def __init__(self, data: dict, requester: HttpRequester) -> None:
        self._requester = requester

        self.id: str = data["api_id"]
        self.calendar_id: str = data["calendar_api_id"]
        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description")
        self.description_md: Optional[str] = data.get("description_md")
        self.cover_url: Optional[str] = data.get("cover_url")
        self.url: Optional[str] = data.get("url")
        self.start_at: datetime = datetime.fromisoformat(data["start_at"].replace("Z", "+00:00"))
        self.end_at: datetime = datetime.fromisoformat(data["end_at"].replace("Z", "+00:00"))
        self.timezone: Optional[str] = data.get("timezone")
        self.visibility: Optional[str] = data.get("visibility")
        self.geo_address: Optional[GeoAddress] = (
            GeoAddress._from_dict(data["geo_address_json"])
            if data.get("geo_address_json")
            else None
        )

    def __repr__(self) -> str:
        return f"<Event id={self.id!r} name={self.name!r}>"
