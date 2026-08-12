from __future__ import annotations

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote
from lote_shared.persistence.lote_repo import LoteRepositorio
from lote_shared.validacao.validadores_cliente import resumir_validacao

from lote_worker.infrastructure.cache_invalidator import CacheInvalidator
from lote_worker.infrastructure.leitor_csv import (
    ArquivoAusente,
    CabecalhoInvalido,
    ler_csv_clientes,
)


class ErroRetentavel(Exception):
    """Falha que deve disparar retry Celery."""


class ProcessadorLote:
    def __init__(
        self,
        repo: LoteRepositorio,
        cache: CacheInvalidator | None = None,
    ) -> None:
        self._repo = repo
        self._cache = cache

    def eh_noop_idempotente(self, lote: Lote, task_id: str | None) -> bool:
        return (
            lote.status == StatusLote.CONCLUIDO
            and task_id is not None
            and lote.celery_task_id == task_id
        )

    def processar(self, lote_id: int, caminho: str, task_id: str | None) -> str:
        lote = self._repo.obter_por_id(lote_id)
        if lote is None:
            raise ErroRetentavel(f"lote {lote_id} nao encontrado")

        if self.eh_noop_idempotente(lote, task_id):
            return "NOOP"

        try:
            resultado = ler_csv_clientes(caminho)
        except ArquivoAusente as exc:
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
