from faststream.rabbit import RabbitBroker

from service.settings import settings
from service.broker.consumer import router as consume_router
from service.service.inventory import router as inventory_router

broker = RabbitBroker(settings.rabbitmq_url)

broker.include_router(consume_router)
broker.include_router(inventory_router)
