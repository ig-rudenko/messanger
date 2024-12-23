# Применение миграций
alembic upgrade head;

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000;
