from pathlib import Path

import pytest

from lote_shared.domain.excecoes import ErroArmazenamento, ObjetoNaoEncontrado
from lote_shared.storage.local import ArmazenamentoArquivoLocal


def test_salvar_retorna_ref_relativa(tmp_path: Path):
    store = ArmazenamentoArquivoLocal(str(tmp_path))
    ref = store.salvar("1_clientes.csv", b"nome,email\n")
    assert ref == "lotes/1_clientes.csv"
    assert not Path(ref).is_absolute()
    assert (tmp_path / ref).is_file()


def test_existe_e_abrir(tmp_path: Path):
    store = ArmazenamentoArquivoLocal(str(tmp_path))
    ref = store.salvar("2_a.csv", b"abc")
    assert store.existe(ref) is True
    assert store.abrir(ref) == b"abc"


def test_abrir_ausente(tmp_path: Path):
    store = ArmazenamentoArquivoLocal(str(tmp_path))
    with pytest.raises(ObjetoNaoEncontrado):
        store.abrir("lotes/nao_existe.csv")


def test_diretorio_obrigatorio():
    with pytest.raises(ErroArmazenamento):
        ArmazenamentoArquivoLocal("")
