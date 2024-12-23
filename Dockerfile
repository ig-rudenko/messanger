FROM python:3.12.8-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade --no-cache-dir pip && \
    pip install -r requirements.txt --no-cache-dir;

RUN addgroup -g 10001 user_app_group \
    && adduser -D -h /app -u 10002 user_app user_app_group \
    && chown -R user_app:user_app_group /app;

COPY --chown=user_app:user_app_group . /app/

USER user_app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
