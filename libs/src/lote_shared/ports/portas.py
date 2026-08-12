from __future__ import annotations

from typing import Protocol, runtime_checkable

from lote_shared.domain.lote import Lote


@runtime_checkable
class PortaLoteRepositorio(Protocol):
    def salvar(self, lote: Lote) -> Lote: ...

    def obter_por_id(self, lote_id: int) -> Lote | None: ...

    def listar_ordenados_por_criacao_desc(self) -> list[Lote]: ...

    def remover(self, lote_id: int) -> bool: ...


@runtime_checkable
class PortaArmazenamentoArquivo(Protocol):
    def salvar(self, nome_destino: str, conteudo: bytes) -> str: ...

    def existe(self, caminho: str) -> bool: ...


@runtime_checkable
class PortaTarefa(Protocol):
    def executar(self, nome_tarefa: str, payload: dict) -> str: ...


@runtime_checkable
class PortaCacheLote(Protocol):
    def obter(self, lote_id: int) -> Lote | None: ...

    def gravar(self, lote: Lote, ttl_segundos: int = 60) -> None: ...

    def invalidar(self, lote_id: int) -> None: ...

    def invalidar_lista(self) -> None: ...
