import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, EmailStr


class Status(StrEnum):
    RESERVED = "reserved"
    OUT_OF_STOCK = "out_of_stock"
    NOT_FOUND = "not_found"
    ERROR = "error"


class OrderItemEvent(BaseModel):
    sku: str
    quantity: int
    price: Decimal


class OrderCreatedEvent(BaseModel):
    order_id: uuid.UUID
    items: list[OrderItemEvent]
    total_price: Decimal
    currency: str
    customer_email: str
    created_at: datetime


class InventoryEvent(BaseModel):
    order_id: uuid.UUID
    status: Status
    customer_email: EmailStr
    failed_sku: str | None = None
    reason: str | None = None
