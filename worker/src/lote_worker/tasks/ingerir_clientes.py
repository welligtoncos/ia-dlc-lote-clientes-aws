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
    return ProcessadorLote(repo, cache, settings=settings)


def _modo_backend(
    caminho: str | None, bucket: str | None, chave: str | None
) -> str:
    if caminho and not bucket and not chave:
        return "fs"
    if bucket and chave and not caminho:
        return "s3"
    return "invalido"


@app.task(bind=True, name="ingerir_clientes", max_retries=3)
def ingerir_clientes(
    self,
    lote_id: int,
    caminho: str | None = None,
    bucket: str | None = None,
    chave: str | None = None,
) -> str:
    """Task allowlisted; kwargs fs {caminho} ou s3 {bucket,chave}.

    Retry Celery com countdown 60/120/240s; marcar_erro so ao esgotar.
    """
    task_id = self.request.id
    tentativa = (self.request.retries or 0) + 1
    backend = _modo_backend(caminho, bucket, chave)
    extra = {
        "task_id": task_id,
        "lote_id": lote_id,
        "tentativa": tentativa,
        "storage_backend": backend,
    }
    logger.info("inicio processamento", extra=extra)

    processador = _processador()
    try:
        if backend == "invalido":
            raise ErroRetentavel(
                "kwargs invalidos: use caminho (fs) ou bucket+chave (s3)"
            )
        status = processador.processar(
            lote_id,
            task_id,
            caminho=caminho,
            bucket=bucket,
            chave=chave,
        )
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
