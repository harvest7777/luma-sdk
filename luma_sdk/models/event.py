from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


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


@dataclass
class Host:
    api_id: str
    name: str
    email: Optional[str]
    avatar_url: Optional[str]

    @classmethod
    def _from_dict(cls, data: dict) -> "Host":
        return cls(
            api_id=data["api_id"],
            name=data.get("name") or "",
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
        )


class Event:
    def __init__(self, data: dict, requester) -> None:
        self._requester = requester
        event = data["event"]

        self.id: str = event["api_id"]
        self.calendar_id: str = event["calendar_api_id"]
        self.name: str = event["name"]
        self.description: Optional[str] = event.get("description")
        self.description_md: Optional[str] = event.get("description_md")
        self.cover_url: Optional[str] = event.get("cover_url")
        self.url: Optional[str] = event.get("url")
        self.start_at: datetime = datetime.fromisoformat(event["start_at"].replace("Z", "+00:00"))
        self.end_at: datetime = datetime.fromisoformat(event["end_at"].replace("Z", "+00:00"))
        self.timezone: Optional[str] = event.get("timezone")
        self.visibility: Optional[str] = event.get("visibility")
        self.geo_address: Optional[GeoAddress] = (
            GeoAddress._from_dict(event["geo_address_json"])
            if event.get("geo_address_json")
            else None
        )
        self.tags: list[str] = event.get("tags") or []
        self.hosts: list[Host] = [Host._from_dict(h) for h in data.get("hosts", [])]

    def __repr__(self) -> str:
        return f"<Event id={self.id!r} name={self.name!r}>"
