from fastapi.testclient import TestClient

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote

from lote_api.application.casos_uso import (
    CasoUsoIngerirClientes,
    CasoUsoListarLotes,
    CasoUsoObterLote,
    CasoUsoRemoverLote,
    CasoUsoReprocessarLote,
)
from lote_api.presentation.app import criar_app


class RepoMemoria:
    def __init__(self) -> None:
        self._dados: dict[int, Lote] = {}
        self._seq = 1

    def salvar(self, lote: Lote) -> Lote:
        if lote.id is None:
            lote.id = self._seq
            self._seq += 1
        self._dados[lote.id] = lote
        return lote

    def obter_por_id(self, lote_id: int):
        return self._dados.get(lote_id)

    def listar_ordenados_por_criacao_desc(self):
        return sorted(self._dados.values(), key=lambda l: l.criado_em, reverse=True)

    def remover(self, lote_id: int) -> bool:
        return self._dados.pop(lote_id, None) is not None


class ArmazenamentoMemoria:
    def __init__(self) -> None:
        self.arquivos: dict[str, bytes] = {}

    def salvar(self, nome_destino: str, conteudo: bytes) -> str:
        caminho = f"/tmp/{nome_destino}"
        self.arquivos[caminho] = conteudo
        return caminho

    def existe(self, caminho: str) -> bool:
        return caminho in self.arquivos


class TarefasOk:
    def executar(self, nome_tarefa: str, payload: dict) -> str:
        return "task-123"


def _client():
    repo, store, tasks = RepoMemoria(), ArmazenamentoMemoria(), TarefasOk()
    app = criar_app(
        CasoUsoIngerirClientes(repo, store, tasks),
        CasoUsoObterLote(repo),
        CasoUsoListarLotes(repo),
        CasoUsoReprocessarLote(repo, store, tasks),
        CasoUsoRemoverLote(repo),
    )
    return TestClient(app), repo, store


def test_health():
    client, _, _ = _client()
    assert client.get("/health").status_code == 200


def test_post_e_get():
    client, _, _ = _client()
    r = client.post(
        "/lotes",
        files={"arquivo": ("clientes.csv", b"nome,email\n", "text/csv")},
    )
    assert r.status_code == 202
    body = r.json()
    assert body["status"] == "PENDENTE"
    assert "X-Request-ID" in r.headers
    g = client.get(f"/lotes/{body['lote_id']}")
    assert g.status_code == 200
    assert g.json()["nome_arquivo"] == "clientes.csv"


def test_delete():
    client, repo, _ = _client()
    lote = repo.salvar(Lote.criar_pendente("a.csv"))
    r = client.delete(f"/lotes/{lote.id}")
    assert r.status_code == 204


def test_reprocessar_409():
    client, repo, _ = _client()
    lote = repo.salvar(Lote.criar_pendente("a.csv"))
    lote.status = StatusLote.CONCLUIDO
    repo.salvar(lote)
    r = client.put(f"/lotes/{lote.id}")
    assert r.status_code == 409
