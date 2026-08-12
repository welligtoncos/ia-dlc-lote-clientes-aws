from __future__ import annotations

import logging

from lote_shared.domain.excecoes import (
    ArquivoAusenteParaReprocessamento,
    ArquivoInvalido,
    LoteNaoEncontrado,
    ReprocessamentoNaoPermitido,
    TamanhoExcedido,
)
from lote_shared.domain.lote import Lote
from lote_shared.ports.portas import (
    PortaArmazenamentoArquivo,
    PortaCacheLote,
    PortaLoteRepositorio,
    PortaTarefa,
)

from lote_api.application.regras_upload import (
    LIMITE_UPLOAD_BYTES,
    TAREFA_INGERIR,
    validar_nome_csv,
)

logger = logging.getLogger(__name__)


class CasoUsoIngerirClientes:
    def __init__(
        self,
        repo: PortaLoteRepositorio,
        armazenamento: PortaArmazenamentoArquivo,
        tarefas: PortaTarefa,
        cache: PortaCacheLote | None = None,
    ) -> None:
        self._repo = repo
        self._armazenamento = armazenamento
        self._tarefas = tarefas
        self._cache = cache

    def executar(self, nome_arquivo: str, conteudo: bytes) -> dict:
        if not conteudo:
            raise ArquivoInvalido("arquivo ausente ou vazio")
        if not validar_nome_csv(nome_arquivo):
            raise ArquivoInvalido("arquivo deve ter extensao .csv")
        if len(conteudo) > LIMITE_UPLOAD_BYTES:
            raise TamanhoExcedido(len(conteudo), LIMITE_UPLOAD_BYTES)

        lote = Lote.criar_pendente(nome_arquivo)
        lote = self._repo.salvar(lote)
        assert lote.id is not None

        destino = f"{lote.id}_{nome_arquivo}"
        caminho = self._armazenamento.salvar(destino, conteudo)
        lote.caminho_arquivo = caminho
        lote = self._repo.salvar(lote)

        task_id = None
        try:
            task_id = self._tarefas.executar(
                TAREFA_INGERIR, {"lote_id": lote.id, "caminho": caminho}
            )
            lote.associar_task(task_id)
            lote = self._repo.salvar(lote)
        except Exception:
            logger.exception(
                "falha no enqueue do lote_id=%s; lote permanece PENDENTE", lote.id
            )

        if self._cache:
            self._cache.invalidar_lista()

        return {
            "lote_id": lote.id,
            "task_id": task_id,
            "status": lote.status.value,
        }


class CasoUsoObterLote:
    def __init__(
        self,
        repo: PortaLoteRepositorio,
        cache: PortaCacheLote | None = None,
    ) -> None:
        self._repo = repo
        self._cache = cache

    def executar(self, lote_id: int) -> Lote:
        if self._cache:
            cached = self._cache.obter(lote_id)
            if cached:
                return cached
        lote = self._repo.obter_por_id(lote_id)
        if lote is None:
            raise LoteNaoEncontrado(lote_id)
        if self._cache:
            self._cache.gravar(lote)
        return lote


class CasoUsoListarLotes:
    def __init__(self, repo: PortaLoteRepositorio) -> None:
        self._repo = repo

    def executar(self) -> list[Lote]:
        return self._repo.listar_ordenados_por_criacao_desc()


class CasoUsoReprocessarLote:
    def __init__(
        self,
        repo: PortaLoteRepositorio,
        armazenamento: PortaArmazenamentoArquivo,
        tarefas: PortaTarefa,
        cache: PortaCacheLote | None = None,
    ) -> None:
        self._repo = repo
        self._armazenamento = armazenamento
        self._tarefas = tarefas
        self._cache = cache

    def executar(self, lote_id: int) -> dict:
        lote = self._repo.obter_por_id(lote_id)
        if lote is None:
            raise LoteNaoEncontrado(lote_id)
        if not lote.pode_reprocessar():
            raise ReprocessamentoNaoPermitido(lote_id, lote.status.value)
        if not lote.caminho_arquivo or not self._armazenamento.existe(
            lote.caminho_arquivo
        ):
            raise ArquivoAusenteParaReprocessamento(
                lote_id, lote.caminho_arquivo or ""
            )

        lote.preparar_reprocessamento()
        lote = self._repo.salvar(lote)

        task_id = None
        try:
            task_id = self._tarefas.executar(
                TAREFA_INGERIR,
                {"lote_id": lote.id, "caminho": lote.caminho_arquivo},
            )
            lote.associar_task(task_id)
            lote = self._repo.salvar(lote)
        except Exception:
            logger.exception(
                "falha no enqueue de reprocessamento lote_id=%s", lote_id
            )

        if self._cache and lote.id is not None:
            self._cache.invalidar(lote.id)

        return {
            "lote_id": lote.id,
            "task_id": task_id,
            "status": lote.status.value,
        }


class CasoUsoRemoverLote:
    def __init__(
        self,
        repo: PortaLoteRepositorio,
        cache: PortaCacheLote | None = None,
    ) -> None:
        self._repo = repo
        self._cache = cache

    def executar(self, lote_id: int) -> None:
        if self._repo.obter_por_id(lote_id) is None:
            raise LoteNaoEncontrado(lote_id)
        self._repo.remover(lote_id)
        if self._cache:
            self._cache.invalidar(lote_id)
