from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from service.models.inventory import Inventory


class InventoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_sku(self, sku: str) -> Inventory | None:
        query = select(Inventory).filter(Inventory.sku == sku)
        item = await self.session.execute(query)
        return item.scalars().one_or_none()

    async def reserve(self, sku: str, quantity: int) -> bool:
        query = (
            update(Inventory)
            .filter(
                Inventory.sku == sku,
                (Inventory.quantity - Inventory.reserved) >= quantity,
            )
            .values(reserved=Inventory.reserved + quantity)
            .returning(Inventory.id)
        )
        result = await self.session.execute(query)
        row = result.first()
        return row is not None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
