"""Validadores de linha de cliente e resumo de qualidade."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


CABECALHO_ESPERADO = ("nome", "email", "cpf", "telefone")


def validar_nome(valor: str | None) -> bool:
    return bool(valor and valor.strip())


def validar_email(valor: str | None) -> bool:
    if not valor or "@" not in valor:
        return False
    usuario, _, dominio = valor.partition("@")
    return bool(usuario.strip()) and "." in dominio


def validar_cpf(valor: str | None) -> bool:
    """CPF valido somente com exatamente 11 caracteres numericos + DV (sem mascara)."""
    if not valor or len(valor) != 11 or not valor.isdigit():
        return False
    if valor == valor[0] * 11:
        return False
    soma = sum(int(valor[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    if d1 == 10:
        d1 = 0
    if d1 != int(valor[9]):
        return False
    soma = sum(int(valor[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    if d2 == 10:
        d2 = 0
    return d2 == int(valor[10])


def validar_telefone(valor: str | None) -> bool:
    if valor is None or valor == "":
        return True
    if not valor.isdigit():
        return False
    return 10 <= len(valor) <= 11


def linha_valida(linha: Mapping[str, str | None]) -> bool:
    return (
        validar_nome(linha.get("nome"))
        and validar_email(linha.get("email"))
        and validar_cpf(linha.get("cpf"))
        and validar_telefone(linha.get("telefone"))
    )


@dataclass(frozen=True)
class ResumoValidacao:
    total_linhas: int
    linhas_validas: int
    linhas_invalidas: int

    def __post_init__(self) -> None:
        if self.total_linhas != self.linhas_validas + self.linhas_invalidas:
            raise ValueError("invariante total != validas + invalidas")


def resumir_validacao(linhas: Iterable[Mapping[str, str | None]]) -> ResumoValidacao:
    total = 0
    validas = 0
    invalidas = 0
    for linha in linhas:
        total += 1
        if linha_valida(linha):
            validas += 1
        else:
            invalidas += 1
    return ResumoValidacao(total, validas, invalidas)
