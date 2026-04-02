from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from service.db import Base


class Inventory(Base):
    __tablename__ = "inventory"

    sku: Mapped[str] = mapped_column(String(50), unique=True)
    quantity: Mapped[int] = mapped_column(default=0)
    reserved: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
