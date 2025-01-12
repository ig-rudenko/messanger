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
            syncers.append(DataBaseSynchronizer())
        if "elasticsearch" in settings.sync_storages_list:
            syncers.append(ElasticsearchSynchronizer())

        while True:
            try:
                await consume_messages_from_queue(syncers)
            except aio_pika.exceptions.AMQPError as exc:
                print(exc)
                await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
