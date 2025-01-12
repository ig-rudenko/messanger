import asyncio

import aio_pika
from asyncio.queues import Queue

from messanger.deco import singleton
from messanger.settings import settings


@singleton
class RabbitMQConnector:

    def __init__(self, url: str):
        self._url = url
        self._connection: None | aio_pika.RobustConnection = None
        self._queue = Queue()

    async def get_connection(self) -> aio_pika.RobustConnection:
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self._url)
        return self._connection

    async def publish_message(self, message: str):
        self._queue.put_nowait(message)

    async def run_publisher(self, exchange: str, routing_key: str, queue_name: str):
        _ = asyncio.create_task(self._run_publisher(exchange, routing_key, queue_name))

    async def _run_publisher(self, exchange: str, routing_key: str, queue_name: str):
        connection = await self.get_connection()
        while True:
            try:
                async with connection:
                    async with connection.channel() as channel:
                        exchange = await channel.declare_exchange(
                            exchange, aio_pika.ExchangeType.DIRECT, durable=True
                        )
                        queue = await channel.declare_queue(name=queue_name, durable=True)
                        await queue.bind(exchange, routing_key)

                        while True:
                            message = await self._queue.get()
                            await exchange.publish(
                                aio_pika.Message(message.encode("utf-8"), content_type="application/json"),
                                routing_key=routing_key,
                            )

            except aio_pika.exceptions.AMQPError as exc:
                print(exc)


rmq_connector = RabbitMQConnector(settings.sync_rabbitmq_url)
