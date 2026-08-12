from __future__ import annotations

from pathlib import Path

import pytest

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote
from lote_worker.application.processador import ErroRetentavel, ProcessadorLote


class RepoMemoria:
    def __init__(self) -> None:
        self.lotes: dict[int, Lote] = {}

    def obter_por_id(self, lote_id: int) -> Lote | None:
        return self.lotes.get(lote_id)

    def salvar(self, lote: Lote) -> Lote:
        if lote.id is None:
            lote.id = max(self.lotes.keys(), default=0) + 1
        self.lotes[lote.id] = lote
        return lote


class CacheFake:
    def __init__(self) -> None:
        self.invalidacoes: list[int] = []

    def invalidar_lote(self, lote_id: int) -> None:
        self.invalidacoes.append(lote_id)


def _csv_ok(tmp_path: Path) -> str:
    p = tmp_path / "ok.csv"
    p.write_text(
        "nome,email,cpf,telefone\n"
        "Maria,maria@ex.com,52998224725,11987654321\n"
        "Ruim,,123,abc\n",
        encoding="utf-8",
    )
    return str(p)


def test_processar_concluido(tmp_path: Path):
    repo = RepoMemoria()
    cache = CacheFake()
    lote = Lote.criar_pendente("ok.csv")
    lote.id = 1
    lote.celery_task_id = "task-1"
    lote.caminho_arquivo = _csv_ok(tmp_path)
    repo.salvar(lote)

    proc = ProcessadorLote(repo, cache)  # type: ignore[arg-type]
    status = proc.processar(1, lote.caminho_arquivo, "task-1")
    assert status == "CONCLUIDO"
    atualizado = repo.obter_por_id(1)
    assert atualizado is not None
    assert atualizado.status == StatusLote.CONCLUIDO
    assert atualizado.total_linhas == 2
    assert atualizado.linhas_validas == 1
    assert atualizado.linhas_invalidas == 1
    assert cache.invalidacoes == [1]


def test_noop_idempotente(tmp_path: Path):
    repo = RepoMemoria()
    lote = Lote.criar_pendente("ok.csv")
    lote.id = 1
    lote.celery_task_id = "task-1"
    lote.marcar_concluido(1, 1, 0)
    repo.salvar(lote)
    proc = ProcessadorLote(repo)  # type: ignore[arg-type]
    assert proc.processar(1, _csv_ok(tmp_path), "task-1") == "NOOP"


def test_cabecalho_invalido_retentavel(tmp_path: Path):
    repo = RepoMemoria()
    lote = Lote.criar_pendente("bad.csv")
    lote.id = 2
    caminho = tmp_path / "bad.csv"
    caminho.write_text("x,y\n1,2\n", encoding="utf-8")
    lote.caminho_arquivo = str(caminho)
    repo.salvar(lote)
    proc = ProcessadorLote(repo)  # type: ignore[arg-type]
    with pytest.raises(ErroRetentavel):
        proc.processar(2, str(caminho), "t2")
    assert repo.obter_por_id(2).status == StatusLote.PENDENTE  # type: ignore[union-attr]


def test_p_val_06_idempotencia_nao_altera_contagens(tmp_path: Path):
    repo = RepoMemoria()
    lote = Lote.criar_pendente("ok.csv")
    lote.id = 3
    lote.celery_task_id = "same"
    lote.marcar_concluido(10, 7, 3)
    repo.salvar(lote)
    proc = ProcessadorLote(repo)  # type: ignore[arg-type]
    proc.processar(3, _csv_ok(tmp_path), "same")
    atual = repo.obter_por_id(3)
    assert atual is not None
    assert atual.total_linhas == 10
    assert atual.linhas_validas == 7
