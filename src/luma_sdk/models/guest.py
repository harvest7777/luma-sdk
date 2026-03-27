from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from luma_sdk.models.base import LumaModel
from luma_sdk.requester import HttpRequester
from luma_sdk.utils.datetime import parse_dt as _parse_dt


@dataclass
class RegistrationAnswer:
    question_id: str
    label: str
    question_type: str
    value: object
    answer: object

    @classmethod
    def _from_dict(cls, data: dict) -> "RegistrationAnswer":
        return cls(
            question_id=data["question_id"],
            label=data["label"],
            question_type=data["question_type"],
            value=data.get("value"),
            answer=data.get("answer"),
        )


@dataclass
class EventTicket:
    id: str
    name: str
    amount: int
    amount_discount: int
    amount_tax: int
    currency: str
    event_ticket_type_id: str
    is_captured: bool
    checked_in_at: Optional[datetime]

    @classmethod
    def _from_dict(cls, data: dict) -> "EventTicket":
        return cls(
            id=data["id"],
            name=data["name"],
            amount=data["amount"],
            amount_discount=data["amount_discount"],
            amount_tax=data["amount_tax"],
            currency=data["currency"],
            event_ticket_type_id=data["event_ticket_type_id"],
            is_captured=data["is_captured"],
            checked_in_at=_parse_dt(data.get("checked_in_at")),
        )


@dataclass
class CouponInfo:
    api_id: str
    code: str
    percent_off: Optional[float]
    cents_off: Optional[int]
    currency: str

    @classmethod
    def _from_dict(cls, data: dict) -> "CouponInfo":
        return cls(
            api_id=data["api_id"],
            code=data["code"],
            percent_off=data.get("percent_off"),
            cents_off=data.get("cents_off"),
            currency=data["currency"],
        )


@dataclass
class EventTicketOrder:
    id: str
    amount: int
    amount_discount: int
    amount_tax: int
    currency: str
    is_captured: bool
    coupon_info: Optional[CouponInfo]

    @classmethod
    def _from_dict(cls, data: dict) -> "EventTicketOrder":
        coupon_raw = data.get("coupon_info")
        return cls(
            id=data["id"],
            amount=data["amount"],
            amount_discount=data["amount_discount"],
            amount_tax=data["amount_tax"],
            currency=data["currency"],
            is_captured=data["is_captured"],
            coupon_info=CouponInfo._from_dict(coupon_raw) if coupon_raw else None,
        )


class Guest(LumaModel):
    def __init__(self, data: dict, requester: HttpRequester) -> None:
        super().__init__(data, requester)

        self.id: str = data["id"]
        self.user_id: str = data["user_id"]
        self.user_email: str = data["user_email"]
        self.user_name: Optional[str] = data.get("user_name")
        self.user_first_name: Optional[str] = data.get("user_first_name")
        self.user_last_name: Optional[str] = data.get("user_last_name")
        self.approval_status: str = data["approval_status"]
        self.check_in_qr_code: str = data["check_in_qr_code"]
        self.custom_source: Optional[str] = data.get("custom_source")
        self.invited_at: Optional[datetime] = _parse_dt(data.get("invited_at"))
        self.joined_at: Optional[datetime] = _parse_dt(data.get("joined_at"))
        self.registered_at: Optional[datetime] = _parse_dt(data.get("registered_at"))
        # Deprecated by Luma API — check_in is moving to EventTicket.checked_in_at
        self.checked_in_at: Optional[datetime] = _parse_dt(data.get("checked_in_at"))
        self.phone_number: Optional[str] = data.get("phone_number")
        self.eth_address: Optional[str] = data.get("eth_address")
        self.solana_address: Optional[str] = data.get("solana_address")
        self.registration_answers: list[RegistrationAnswer] = [
            RegistrationAnswer._from_dict(a) for a in (data.get("registration_answers") or [])
        ]
        self.event_tickets: list[EventTicket] = [
            EventTicket._from_dict(t) for t in (data.get("event_tickets") or [])
        ]
        self.event_ticket_orders: list[EventTicketOrder] = [
            EventTicketOrder._from_dict(o) for o in (data.get("event_ticket_orders") or [])
        ]

    def __repr__(self) -> str:
        return f"<Guest id={self.id!r} email={self.user_email!r}>"
