FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uvicorn fastapi pydantic pydantic-settings python-multipart \
    "celery[redis]" sqlalchemy pymysql redis

COPY libs /app/libs
RUN pip install --no-cache-dir -e /app/libs

COPY api /app/api
RUN pip install --no-cache-dir -e /app/api

ENV PYTHONPATH=/app/api/src:/app/libs/src
WORKDIR /app/api

CMD ["uvicorn", "lote_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
