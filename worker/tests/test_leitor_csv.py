from pathlib import Path

import pytest

from lote_worker.infrastructure.leitor_csv import (
    CabecalhoInvalido,
    ler_csv_clientes,
    ler_csv_clientes_de_bytes,
)


def test_ler_csv_com_bom(tmp_path: Path):
    arquivo = tmp_path / "c.csv"
    arquivo.write_bytes(
        b"\xef\xbb\xbfnome,email,cpf,telefone\n"
        b"Ana,ana@ex.com,52998224725,11999999999\n"
    )
    resultado = ler_csv_clientes(str(arquivo))
    assert len(resultado.linhas) == 1
    assert resultado.linhas[0]["nome"] == "Ana"


def test_ignora_linha_em_branco(tmp_path: Path):
    arquivo = tmp_path / "c.csv"
    arquivo.write_text(
        "nome,email,cpf,telefone\n\n  \nJoao,j@ex.com,52998224725,\n",
        encoding="utf-8",
    )
    resultado = ler_csv_clientes(str(arquivo))
    assert len(resultado.linhas) == 1


def test_cabecalho_invalido(tmp_path: Path):
    arquivo = tmp_path / "c.csv"
    arquivo.write_text("a,b,c\n1,2,3\n", encoding="utf-8")
    with pytest.raises(CabecalhoInvalido):
        ler_csv_clientes(str(arquivo))


def test_ler_csv_de_bytes_com_bom():
    conteudo = (
        b"\xef\xbb\xbfnome,email,cpf,telefone\n"
        b"Ana,ana@ex.com,52998224725,11999999999\n"
    )
    resultado = ler_csv_clientes_de_bytes(conteudo)
    assert len(resultado.linhas) == 1
    assert resultado.linhas[0]["nome"] == "Ana"
