from faststream import FastStream

from service.broker.broker import broker
from service.broker.consumer import router as consumer_router
from service.service.inventory import router as publisher_router

broker.include_router(consumer_router)
broker.include_router(publisher_router)


app = FastStream(broker)
