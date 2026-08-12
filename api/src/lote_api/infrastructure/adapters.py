from __future__ import annotations

from pathlib import Path

from lote_shared.domain.excecoes import TarefaNaoPermitida


TAREFAS_SUPORTADAS = {"ingerir_clientes"}


class ArmazenamentoArquivoLocal:
    def __init__(self, diretorio: str) -> None:
        self._dir = Path(diretorio)
        self._dir.mkdir(parents=True, exist_ok=True)

    def salvar(self, nome_destino: str, conteudo: bytes) -> str:
        caminho = self._dir / nome_destino
        caminho.write_bytes(conteudo)
        return str(caminho)

    def existe(self, caminho: str) -> bool:
        return Path(caminho).is_file()


class AdaptadorCelery:
    """Enqueue Celery com allowlist; propaga excecoes para o caso de uso (degraded)."""

    def __init__(self, broker_url: str) -> None:
        from celery import Celery

        self._app = Celery("lote_api", broker=broker_url)

    def executar(self, nome_tarefa: str, payload: dict) -> str:
        if nome_tarefa not in TAREFAS_SUPORTADAS:
            raise TarefaNaoPermitida(nome_tarefa)
        async_result = self._app.send_task(nome_tarefa, kwargs=payload)
        return async_result.id
