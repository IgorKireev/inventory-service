from faststream import FastStream

from service.broker.broker import broker

app = FastStream(broker)
