import asyncio

import aio_pika

from messanger.orm.session_manager import db_manager
from messanger.synchronizer.consumer import consume_messages_from_queue
from messanger.synchronizer.sync import DataBaseSynchronizer, ElasticsearchSynchronizer
from messanger.settings import settings


async def main():
    db_manager.init(settings.database_url)

    while True:
        syncers = []
        if "database" in settings.sync_storages_list:
            print("Используется синхронизатор: База данных")
            syncers.append(DataBaseSynchronizer())
        if "elasticsearch" in settings.sync_storages_list:
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
