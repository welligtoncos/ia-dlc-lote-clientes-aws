from __future__ import annotations

from lote_shared.persistence.lote_repo import LoteRepositorio, criar_session_factory

from lote_worker.application.processador import ErroRetentavel, ProcessadorLote
from lote_worker.celery_app import app, get_settings
from lote_worker.infrastructure.cache_invalidator import CacheInvalidator
from lote_worker.logging_json import configurar_logging

COUNTDOWNS = (60, 120, 240)
logger = configurar_logging()


def _processador() -> ProcessadorLote:
    settings = get_settings()
    repo = LoteRepositorio(criar_session_factory(settings.database_url))
    cache = CacheInvalidator(settings.cache_url)
    return ProcessadorLote(repo, cache)


@app.task(bind=True, name="ingerir_clientes", max_retries=3)
def ingerir_clientes(self, lote_id: int, caminho: str) -> str:
    """Task allowlisted; kwargs alinhados ao send_task da API.

    Retry Celery com countdown 60/120/240s (RNF-03); marcar_erro so ao esgotar.
    """
    task_id = self.request.id
    tentativa = (self.request.retries or 0) + 1
    extra = {"task_id": task_id, "lote_id": lote_id, "tentativa": tentativa}
    logger.info("inicio processamento", extra=extra)

    processador = _processador()
    try:
        status = processador.processar(lote_id, caminho, task_id)
        logger.info(
            "fim processamento",
            extra={**extra, "status_final": status},
        )
        return status
    except ErroRetentavel as exc:
        if (self.request.retries or 0) >= self.max_retries:
            processador.marcar_erro_terminal(lote_id, str(exc))
            logger.error(
                "erro terminal apos retries",
                extra={**extra, "status_final": "ERRO"},
            )
            return "ERRO"
        countdown = COUNTDOWNS[min(self.request.retries or 0, len(COUNTDOWNS) - 1)]
        logger.warning(
            "falha retentavel",
            extra={**extra, "status_final": "RETRY"},
        )
        raise self.retry(exc=exc, countdown=countdown) from exc
