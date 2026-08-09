from faststream import Depends
from faststream.rabbit import RabbitRouter

from service.dependency import get_inventory_service
from service.queue import order_q
from service.schemas.event_schema import OrderCreatedEvent
from service.service.inventory import InventoryService


router = RabbitRouter()


@router.subscriber(
    queue=order_q[0],
    exchange=order_q[1],
)
async def handle_order_created(
    message: OrderCreatedEvent,
    service: InventoryService = Depends(get_inventory_service),
) -> None:
    await service.process_order(message)
