from __future__ import annotations

from typing import Any

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote
from lote_shared.persistence.lote_repo import LoteRepositorio
from lote_shared.validacao.validadores_cliente import resumir_validacao

from lote_worker.infrastructure.cache_invalidator import CacheInvalidator
from lote_worker.infrastructure.leitor_csv import (
    ArquivoAusente,
    CabecalhoInvalido,
    ModoTarefaInvalido,
    carregar_csv_clientes,
)


class ErroRetentavel(Exception):
    """Falha que deve disparar retry Celery."""


class ProcessadorLote:
    def __init__(
        self,
        repo: LoteRepositorio,
        cache: CacheInvalidator | None = None,
        settings: Any | None = None,
    ) -> None:
        self._repo = repo
        self._cache = cache
        self._settings = settings

    def eh_noop_idempotente(self, lote: Lote, task_id: str | None) -> bool:
        return (
            lote.status == StatusLote.CONCLUIDO
            and task_id is not None
            and lote.celery_task_id == task_id
        )

    def processar(
        self,
        lote_id: int,
        task_id: str | None,
        *,
        caminho: str | None = None,
        bucket: str | None = None,
        chave: str | None = None,
        armazenamento: Any | None = None,
    ) -> str:
        lote = self._repo.obter_por_id(lote_id)
        if lote is None:
            raise ErroRetentavel(f"lote {lote_id} nao encontrado")

        if self.eh_noop_idempotente(lote, task_id):
            return "NOOP"

        try:
            resultado = carregar_csv_clientes(
                caminho=caminho,
                bucket=bucket,
                chave=chave,
                settings=self._settings,
                armazenamento=armazenamento,
            )
        except (ArquivoAusente, ModoTarefaInvalido) as exc:
            raise ErroRetentavel(str(exc)) from exc
        except CabecalhoInvalido as exc:
            raise ErroRetentavel(str(exc)) from exc

        lote.marcar_processando()
        self._repo.salvar(lote)

        resumo = resumir_validacao(resultado.linhas)
        lote.marcar_concluido(
            resumo.total_linhas, resumo.linhas_validas, resumo.linhas_invalidas
        )
        self._repo.salvar(lote)
        if self._cache:
            self._cache.invalidar_lote(lote_id)
        return "CONCLUIDO"

    def marcar_erro_terminal(self, lote_id: int, mensagem: str) -> None:
        lote = self._repo.obter_por_id(lote_id)
        if lote is None:
            return
        lote.marcar_erro(mensagem)
        self._repo.salvar(lote)
        if self._cache:
            self._cache.invalidar_lote(lote_id)
