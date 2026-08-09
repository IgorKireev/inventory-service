from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue

order_q = (
    RabbitQueue(
        name="inventory.q.order.created",
        routing_key="inventory.order.created",
        durable=True,
    ),
    RabbitExchange(
        "orders",
        type=ExchangeType.FANOUT,
        durable=True,
    ),
)

inventory_q = (
    RabbitQueue(
        "inventory.q.payment",
        routing_key="payment.order.reserved",
        durable=True,
    ),
    RabbitQueue(
        "inventory.q.notification",
        routing_key="notification.order.failed",
        durable=True,
    ),
    RabbitExchange(
        name="inventory",
        durable=True,
    ),
)
