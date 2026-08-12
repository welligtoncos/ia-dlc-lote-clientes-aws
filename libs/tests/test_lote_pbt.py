from hypothesis import given, strategies as st

from lote_shared.domain.lote import Lote
from lote_shared.domain.status_lote import StatusLote


@given(st.text(min_size=1).filter(lambda s: s.strip() != ""))
def test_p_api_02_criar_pendente(nome: str):
    lote = Lote.criar_pendente(nome)
    assert lote.status == StatusLote.PENDENTE
    assert lote.total_linhas == 0
    assert lote.linhas_validas == 0
    assert lote.linhas_invalidas == 0


@given(st.sampled_from(list(StatusLote)))
def test_p_api_01_pode_reprocessar_iff_erro(status: StatusLote):
    lote = Lote.criar_pendente("x.csv")
    lote.status = status
    assert lote.pode_reprocessar() is (status == StatusLote.ERRO)


def test_p_api_03_reprocessar_nao_erro_falha():
    lote = Lote.criar_pendente("x.csv")
    lote.status = StatusLote.CONCLUIDO
    assert lote.pode_reprocessar() is False


@given(st.integers(min_value=1, max_value=10_000), st.text(min_size=1, max_size=40))
def test_p_api_04_nome_destino_contem_id(lote_id: int, nome: str):
    nome_limpo = nome.replace("/", "_").replace("\\", "_")
    destino = f"{lote_id}_{nome_limpo}"
    assert destino.startswith(f"{lote_id}_")
