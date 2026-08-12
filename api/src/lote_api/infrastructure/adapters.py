from __future__ import annotations

import logging

from lote_shared.domain.excecoes import TarefaNaoPermitida


TAREFAS_SUPORTADAS = {"ingerir_clientes"}
logger = logging.getLogger(__name__)


class AdaptadorCelery:
    """Enqueue Celery com allowlist; traduz ref -> kwargs fs|s3."""

    def __init__(
        self,
        broker_url: str,
        storage_backend: str = "fs",
        s3_bucket: str = "",
    ) -> None:
        from celery import Celery

        self._app = Celery("lote_api", broker=broker_url)
        self._storage_backend = (storage_backend or "fs").strip().lower()
        self._s3_bucket = s3_bucket or ""
        if self._storage_backend == "s3" and not self._s3_bucket:
            raise ValueError("S3_BUCKET obrigatorio quando STORAGE_BACKEND=s3")

    def _montar_kwargs(self, payload: dict) -> dict:
        lote_id = payload["lote_id"]
        ref = payload.get("ref") or payload.get("caminho")
        if ref is None:
            raise ValueError("payload da tarefa exige ref ou caminho")
        if self._storage_backend == "s3":
            return {
                "lote_id": lote_id,
                "bucket": self._s3_bucket,
                "chave": ref,
            }
        return {"lote_id": lote_id, "caminho": ref}

    def executar(self, nome_tarefa: str, payload: dict) -> str:
        if nome_tarefa not in TAREFAS_SUPORTADAS:
            raise TarefaNaoPermitida(nome_tarefa)
        kwargs = self._montar_kwargs(payload)
        logger.info(
            "enqueue tarefa=%s lote_id=%s backend=%s",
            nome_tarefa,
            kwargs.get("lote_id"),
            self._storage_backend,
        )
        async_result = self._app.send_task(nome_tarefa, kwargs=kwargs)
        return async_result.id
