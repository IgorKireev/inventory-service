import uuid
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


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


class InventoryCheckedEvent(BaseModel):
    order_id: uuid.UUID
    status: str = "confirmed"


class InventoryFailedEvent(BaseModel):
    order_id: uuid.UUID
    reason: str
    failed_sku: str