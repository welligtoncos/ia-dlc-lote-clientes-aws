FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "celery[redis]" pydantic-settings sqlalchemy pymysql redis

COPY libs /app/libs
RUN pip install --no-cache-dir -e /app/libs

COPY worker /app/worker
RUN pip install --no-cache-dir -e /app/worker

ENV PYTHONPATH=/app/worker/src:/app/libs/src
WORKDIR /app/worker

CMD ["celery", "-A", "lote_worker.celery_app", "worker", "--loglevel=INFO", "--concurrency=2"]
