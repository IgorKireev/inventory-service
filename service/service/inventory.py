from faststream.rabbit import RabbitRouter
from service.repository.inventory import InventoryRepository
from service.schemas.event_schema import (
    InventoryEvent,
    OrderCreatedEvent,
    Status,
)
from service.queue import inventory_q


router = RabbitRouter()
router_publisher = router.publisher(
    exchange=inventory_q[2],
)


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    async def process_order(self, event: OrderCreatedEvent) -> None:
        try:
            for item in event.items:
                inventory = await self.repository.get_by_sku(item.sku)

                if not inventory:
                    await router_publisher.publish(
                        InventoryEvent(
                            order_id=event.order_id,
                            status=Status.NOT_FOUND,
                            total_price=event.total_price,
                            failed_sku=item.sku,
                            reason=f"SKU {item.sku} not found",
                            customer_email=event.customer_email,
                        ),
                        exchange=inventory_q[2],
                        routing_key=inventory_q[1].routing_key,
                    )
                    return

                available = inventory.quantity - inventory.reserved
                if available < item.quantity:
                    await router_publisher.publish(
                        InventoryEvent(
                            order_id=event.order_id,
                            status=Status.OUT_OF_STOCK,
                            total_price=event.total_price,
                            failed_sku=item.sku,
                            reason=f"Not enough stock for {item.sku}",
                            customer_email=event.customer_email,
                        ),
                        exchange=inventory_q[2],
                        routing_key=inventory_q[1].routing_key,
                    )
                    return

            for item in event.items:
                reserved = await self.repository.reserve(item.sku, item.quantity)
                if not reserved:
                    await self.repository.rollback()
                    await router_publisher.publish(
                        InventoryEvent(
                            order_id=event.order_id,
                            status=Status.OUT_OF_STOCK,
                            total_price=event.total_price,
                            failed_sku=item.sku,
                            reason="Reserve failed",
                            customer_email=event.customer_email,
                        ),
                        exchange=inventory_q[2],
                        routing_key=inventory_q[1].routing_key,
                    )
                    return

            await self.repository.commit()

            await router_publisher.publish(
                InventoryEvent(
                    order_id=event.order_id,
                    status=Status.RESERVED,
                    total_price=event.total_price,
                    customer_email=event.customer_email,
                ),
                exchange=inventory_q[2],
                routing_key=inventory_q[0].routing_key,
            )

        except Exception:
            await self.repository.rollback()
            await router_publisher.publish(
                InventoryEvent(
                    order_id=event.order_id,
                    status=Status.ERROR,
                    total_price=event.total_price,
                    reason="Internal error",
                    customer_email=event.customer_email,
                ),
                exchange=inventory_q[2],
                routing_key=inventory_q[1].routing_key,
            )
