# 📫 Messenger

Простой мессенджер для общения.

[![](https://skillicons.dev/icons?i=vite,vue,tailwind,python,fastapi,redis,rabbitmq)](https://skillicons.dev)

![diag.svg](docs/img/diag.png)

![img.png](docs/img/img.png)

![img_1.png](docs/img/img_1.png)


## ⚙️ Настройка и запуск

### 🌐 FastAPI

Приложение состоит из чата и API. Запуск.

```shell
# Применение миграций
export DATABASE_URL=postgresql+asyncpg://msg_user:msg_password@database:5432/msg_db
alembic upgrade head;

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000;
```

Переменные окружения для запуска приложения FastAPI:

```dotenv
# Контроль JWT.
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_HOURS=168

# Доступны: "local" и "redis"
# Broadcast отвечает за обмен сообщениями между пользователями.
# Если выбран local - то можно будет обмениваться только в рамкаж одного процесса.
# Для нескольких процессов (инстансов приложения) нужно использовать redis. 
BROADCAST_TYPE=local

# Если BROADCAST_TYPE=redis
BROADCAST_REDIS_URL=redis://redishost:6379/0
BROADCAST_REDIS_MAX_CONNECTIONS=10

REDIS_CACHE_URL=redis://rediscache:6379/0
REDIS_CACHE_MAX_CONNECTIONS=10

# Подключение к базе вместе с асинхронным драйвером.
DATABASE_URL=postgresql+asyncpg://msg_user:msg_password@databasehost:6432/msg_db
DATABASE_MAX_CONNECTIONS=10

# Доступны: "no_storage", "db_direct", "rabbitmq".
# no_storage - не сохраняет сообщения. После перезагрузки страницы они пропадут (анонимный мод).
# db_direct - записывает новые сообщения сразу в базу данных по одному (не производительно)
# rabbitmq - передает новые сообщения в очередь RabbitMQ, дальнейшим сохранением не занимается (производительно).
MESSAGE_STORAGE_TYPE=database

# Если был выбран "rabbitmq", то нужно дополнительно указать переменные подключения к RabbitMQ:
SYNC_RABBITMQ_URL=amqp://msg_user:msg_password@rmq:5672/
SYNC_RABBITMQ_MAX_CONNECTIONS=10
SYNC_RABBITMQ_EXCHANGE=messenger
SYNC_RABBITMQ_ROUTING_KEY=messenger
SYNC_RABBITMQ_QUEUE_NAME=messenger
```

### 🔄 Synchronizer

Если используется RabbitMQ для сохранения сообщений через очередь, нужно запустить синхронизатор.
Он будет брать новые сообщения из очереди и сохранять в указанное хранилище.

```shell
python synchronizer.py
```


Переменные окружения для запуска:

```dotenv
# Через запятую несколько: "database", "elasticsearch"
SYNC_STORAGES=database

# Если было выбрано хранилище "database", нужно указать также переменную окружения:
DATABASE_URL=postgresql+asyncpg://msg_user:msg_password@databasehost:6432/msg_db

# Если было выбрано хранилище "elasticsearch", нужно указать также переменную окружения:
ELASTICSEARCH_HOSTS=http://localhost:9200

# Сохраняет новые подключения только после достижения лимита.
# Увеличивайте согласно вашим нагрузкам.
SYNC_BULK_SIZE=3

# Подключения к RabbitMQ
SYNC_RABBITMQ_URL=amqp://msg_user:msg_password@rmq:5672/
SYNC_RABBITMQ_MAX_CONNECTIONS=10
SYNC_RABBITMQ_EXCHANGE=messenger
SYNC_RABBITMQ_ROUTING_KEY=messenger
SYNC_RABBITMQ_QUEUE_NAME=messenger
```