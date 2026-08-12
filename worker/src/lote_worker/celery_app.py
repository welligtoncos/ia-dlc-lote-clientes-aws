from __future__ import annotations

import os

from celery import Celery

from lote_worker.settings import carregar_settings

_settings = None


def get_settings():
    global _settings
    if _settings is None:
        _settings = carregar_settings()
    return _settings


def criar_celery_app(broker_url: str | None = None) -> Celery:
    url = broker_url or os.environ.get(
        "CELERY_BROKER_URL", "redis://localhost:6379/0"
    )
    app = Celery("lote_worker", broker=url)
    app.conf.update(
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        task_ignore_result=True,
        result_backend=None,
        imports=("lote_worker.tasks.ingerir_clientes",),
    )
    return app


app = criar_celery_app()
