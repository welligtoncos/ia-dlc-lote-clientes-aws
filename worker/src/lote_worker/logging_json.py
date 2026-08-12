from __future__ import annotations

import json
import logging
import sys
import time
from contextlib import contextmanager
from typing import Iterator


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "nivel": record.levelname,
            "mensagem": record.getMessage(),
            "logger": record.name,
        }
        for campo in (
            "task_id",
            "lote_id",
            "tentativa",
            "duracao_ms",
            "status_final",
        ):
            if hasattr(record, campo):
                payload[campo] = getattr(record, campo)
        return json.dumps(payload, ensure_ascii=False)


def configurar_logging(nivel: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("lote_worker")
    logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(nivel.upper())
    logger.propagate = False
    return logger


@contextmanager
def log_contexto(
    logger: logging.Logger,
    *,
    task_id: str | None,
    lote_id: int | None,
    tentativa: int,
) -> Iterator[logging.LoggerAdapter]:
    inicio = time.perf_counter()
    adapter = logging.LoggerAdapter(
        logger,
        {"task_id": task_id, "lote_id": lote_id, "tentativa": tentativa},
    )
    try:
        yield adapter
    finally:
        duracao = int((time.perf_counter() - inicio) * 1000)
        adapter.extra["duracao_ms"] = duracao  # type: ignore[index]
