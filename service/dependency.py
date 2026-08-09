from faststream import Depends

from service.db.accessor import get_session
from service.repository.inventory import InventoryRepository
from service.service.inventory import InventoryService


async def get_inventory_service(
    session=Depends(get_session),
) -> InventoryService:
    return InventoryService(InventoryRepository(session))
