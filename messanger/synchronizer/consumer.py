import aio_pika
from pydantic import ValidationError

from messanger.settings import settings
from messanger.rmq import rmq_connector
from messanger.sockets.schemas import MessageResponseSchema
from .sync import BaseSynchronizer


# Консьюмер сообщений с буферизацией
async def consume_messages_from_queue(syncs: list[BaseSynchronizer]):
    connection = await rmq_connector.get_connection()
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            settings.sync_rabbitmq_exchange, aio_pika.ExchangeType.DIRECT, durable=True
        )
        queue = await channel.declare_queue(settings.sync_rabbitmq_queue_name, durable=True)
        await queue.bind(exchange=exchange, routing_key=settings.sync_rabbitmq_routing_key)

        buffer = []  # Буфер для хранения сообщений

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:  # type: aio_pika.abc.AbstractIncomingMessage
                buffer.append(message)

                # Если в буфере накопились сообщения
                if len(buffer) >= settings.sync_bulk_size:

                    messages = []
                    for msg in buffer:
                        try:
                            messages.append(
                                MessageResponseSchema.model_validate_json(msg.body.decode("utf-8"))
                            )
                        except ValidationError as exc:
                            await msg.reject()
                            print(f"Ошибка при обработке сообщения: {exc}")
                            buffer.remove(msg)

                    # Обрабатываем сообщения
                    sync_success = True
                    for sync in syncs:
                        try:
                            await sync.synchronize(messages)
                        except Exception as exc:
                            print(f"Ошибка при синхронизации: {exc}")
                            sync_success = False

                    if sync_success:
                        # Подтверждаем обработку сообщений
                        for msg in buffer:
                            await msg.ack()
                    else:
                        for msg in buffer:
                            await msg.nack(requeue=True)

                    # Очищаем буфер
                    buffer.clear()
