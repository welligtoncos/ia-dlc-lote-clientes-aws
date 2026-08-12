from lote_shared.domain.excecoes import (
    ArquivoInvalido,
    LoteNaoEncontrado,
    ReprocessamentoNaoPermitido,
    TamanhoExcedido,
)
from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote

from lote_api.application.casos_uso import (
    CasoUsoIngerirClientes,
    CasoUsoObterLote,
    CasoUsoRemoverLote,
    CasoUsoReprocessarLote,
)
from lote_api.application.regras_upload import LIMITE_UPLOAD_BYTES


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
        return sorted(
            self._dados.values(), key=lambda l: l.criado_em, reverse=True
        )

    def remover(self, lote_id: int) -> bool:
        return self._dados.pop(lote_id, None) is not None


class ArmazenamentoMemoria:
    def __init__(self) -> None:
        self.arquivos: dict[str, bytes] = {}

    def salvar(self, nome_destino: str, conteudo: bytes) -> str:
        caminho = f"lotes/{nome_destino}"
        self.arquivos[caminho] = conteudo
        return caminho

    def existe(self, caminho: str) -> bool:
        return caminho in self.arquivos

    def abrir(self, caminho: str) -> bytes:
        return self.arquivos[caminho]


class TarefasOk:
    def executar(self, nome_tarefa: str, payload: dict) -> str:
        return "task-123"


class TarefasFalha:
    def executar(self, nome_tarefa: str, payload: dict) -> str:
        raise RuntimeError("broker down")


def test_ingerir_sucesso():
    repo, store, tasks = RepoMemoria(), ArmazenamentoMemoria(), TarefasOk()
    uc = CasoUsoIngerirClientes(repo, store, tasks)
    out = uc.executar("clientes.csv", b"nome,email,cpf,telefone\n")
    assert out["status"] == "PENDENTE"
    assert out["task_id"] == "task-123"
    assert out["lote_id"] == 1


def test_ingerir_broker_falha_ainda_pendente():
    repo, store = RepoMemoria(), ArmazenamentoMemoria()
    uc = CasoUsoIngerirClientes(repo, store, TarefasFalha())
    out = uc.executar("clientes.csv", b"abc")
    assert out["status"] == "PENDENTE"
    assert out["task_id"] is None


def test_ingerir_tamanho_excedido():
    uc = CasoUsoIngerirClientes(RepoMemoria(), ArmazenamentoMemoria(), TarefasOk())
    try:
        uc.executar("a.csv", b"x" * (LIMITE_UPLOAD_BYTES + 1))
        assert False
    except TamanhoExcedido:
        pass


def test_ingerir_extensao_invalida():
    uc = CasoUsoIngerirClientes(RepoMemoria(), ArmazenamentoMemoria(), TarefasOk())
    try:
        uc.executar("a.txt", b"x")
        assert False
    except ArquivoInvalido:
        pass


def test_obter_nao_encontrado():
    try:
        CasoUsoObterLote(RepoMemoria()).executar(99)
        assert False
    except LoteNaoEncontrado:
        pass


def test_reprocessar_somente_erro():
    repo, store = RepoMemoria(), ArmazenamentoMemoria()
    lote = repo.salvar(Lote.criar_pendente("a.csv"))
    lote.status = StatusLote.CONCLUIDO
    repo.salvar(lote)
    uc = CasoUsoReprocessarLote(repo, store, TarefasOk())
    try:
        uc.executar(lote.id)
        assert False
    except ReprocessamentoNaoPermitido:
        pass


def test_remover():
    repo = RepoMemoria()
    lote = repo.salvar(Lote.criar_pendente("a.csv"))
    CasoUsoRemoverLote(repo).executar(lote.id)
    assert repo.obter_por_id(lote.id) is None
