# inventory-service

Microservice responsible for stock management in the **order-flow** system. Receives order events, checks product availability, reserves stock, and publishes the result downstream.

## Responsibility

- Subscribe to `OrderCreatedEvent` from the `orders` exchange
- Check stock availability for each SKU in the order
- Reserve stock if all items are available
- Publish `InventoryCheckedEvent` to the `inventory` exchange:
  - `RESERVED` → routed to `payment-service`
  - `NOT_FOUND` / `OUT_OF_STOCK` / `ERROR` → routed to `notification-service`

## Message Contracts

### Consumes

- **Exchange:** `orders` (FANOUT)
- **Queue:** `inventory.q.order.created`

**Payload:**
```json
{
  "order_id": "uuid4",
  "items": [
    {
      "sku": "string",
      "quantity": "int",
      "price": "decimal"
    }
  ],
  "total_price": "decimal",
  "currency": "USD | EUR | RUB",
  "customer_email": "email",
  "created_at": "datetime"
}
```