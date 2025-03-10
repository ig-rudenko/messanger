import asyncio

import aio_pika

from messenger.orm.session_manager import db_manager
from messenger.synchronizer.consumer import consume_messages_from_queue
from messenger.synchronizer.sync import DataBaseSynchronizer, ElasticsearchSynchronizer
from messenger.settings import settings


async def main():
    db_manager.init(settings.database_url, pool_size=settings.database_max_connections)

    while True:
        syncers = []
        if "database" in settings.sync.storages_list:
            print("Используется синхронизатор: База данных")
            syncers.append(DataBaseSynchronizer())
        if "elasticsearch" in settings.sync.storages_list:
            print("Используется синхронизатор: Elasticsearch")
            syncers.append(ElasticsearchSynchronizer())

        while True:
            try:
                print("Запуск синхронизатора")
                await consume_messages_from_queue(syncers)
            except aio_pika.exceptions.AMQPError as exc:
                print(f"Ошибка при получении сообщений: {exc}")
                await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
