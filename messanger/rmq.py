import asyncio
from itertools import cycle
from typing import Iterator, NamedTuple, Literal

import aio_pika
from asyncio.queues import Queue

from messanger.deco import singleton
from messanger.settings import settings


class ExchangeChannelPair(NamedTuple):
    channel: aio_pika.abc.AbstractChannel
    exchange: aio_pika.abc.AbstractExchange


class RabbitMQConnector:

    def __init__(self, url: str, exchange: str, routing_key: str, queue_name: str, pool_size: int = 5):
        self._url = url
        self._connection: None | aio_pika.RobustConnection = None
        self._cycle: Iterator[ExchangeChannelPair] | None = None
        self._pool_size = pool_size
        self._queue = Queue()
        self._publisher_is_run = False

        self._exchange_name = exchange
        self._routing_key = routing_key
        self._queue_name = queue_name

    async def publish_message(self, message: str) -> None:
        self._queue.put_nowait(message)

    async def run_publisher(self) -> None:
        if not self._publisher_is_run:
            await self._init_exchanges_pool()
            await self.create_queue()
            _ = asyncio.create_task(self._run_publisher())
            self._publisher_is_run = True

    async def create_queue(self) -> aio_pika.abc.AbstractQueue:
        channel = await self._get_channel()
        queue = await channel.declare_queue(name=self._queue_name, durable=True)
        await queue.bind(self._exchange_name, self._routing_key)
        return queue

    async def _run_publisher(self) -> None:
        while True:
            try:
                message = await self._queue.get()
                exchange = await self._get_exchange()
                await exchange.publish(
                    aio_pika.Message(message.encode("utf-8"), content_type="application/json"),
                    routing_key=self._routing_key,
                )

            except aio_pika.exceptions.AMQPError as exc:
                print(f"Failed to publish message: {exc}")

    async def _init_exchanges_pool(self) -> None:
        """Initialize a pool of channels."""
        connection = await self._get_connection()
        cycle_data = []

        for _ in range(self._pool_size):
            channel = await connection.channel()
            cycle_data.append(
                ExchangeChannelPair(
                    channel=channel,
                    exchange=await channel.declare_exchange(
                        self._exchange_name, type=aio_pika.ExchangeType.DIRECT, durable=True
                    ),
                )
            )
        self._cycle = cycle(cycle_data)

    async def _get_connection(self) -> aio_pika.RobustConnection:
        """Ensure the connection is active, reconnect if necessary."""
        if self._connection is None or self._connection.is_closed:
            try:
                self._connection = await aio_pika.connect_robust(self._url)
            except aio_pika.exceptions.AMQPConnectionError as exc:
                print(f"Failed to connect to RabbitMQ: {exc}")
                self._connection = None
                await asyncio.sleep(2)
        return self._connection

    async def _get_exchange(self) -> aio_pika.abc.AbstractExchange:
        """Get a working channel from the pool."""
        return await self._get_channel_or_exchange("exchange")

    async def _get_channel(self) -> aio_pika.abc.AbstractChannel:
        """Get a working channel from the pool."""
        return await self._get_channel_or_exchange("channel")

    async def _get_channel_or_exchange(self, name: Literal["channel", "exchange"]):
        if not self._cycle:
            await self._init_exchanges_pool()

        for _ in range(self._pool_size):
            data: ExchangeChannelPair = next(self._cycle)
            if not data.channel.is_closed:
                return getattr(data, name)

        await self._init_exchanges_pool()
        return getattr(next(self._cycle), name)


rmq_connector = RabbitMQConnector(
    settings.sync_rabbitmq_url,
    exchange=settings.sync_rabbitmq_exchange,
    routing_key=settings.sync_rabbitmq_routing_key,
    queue_name=settings.sync_rabbitmq_queue_name,
)
