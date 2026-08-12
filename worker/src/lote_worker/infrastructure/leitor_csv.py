from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from lote_shared.validacao.validadores_cliente import CABECALHO_ESPERADO


class CabecalhoInvalido(Exception):
    pass


class ArquivoAusente(Exception):
    pass


@dataclass
class ResultadoLeitura:
    linhas: list[dict[str, str]]


def _normalizar_header(celulas: list[str]) -> tuple[str, ...]:
    normalizadas = []
    for i, c in enumerate(celulas):
        valor = c.strip().lstrip("\ufeff") if i == 0 else c.strip()
        normalizadas.append(valor.lower())
    return tuple(normalizadas)


def ler_csv_clientes(caminho: str) -> ResultadoLeitura:
    path = Path(caminho)
    if not path.is_file():
        raise ArquivoAusente(caminho)

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise CabecalhoInvalido("arquivo vazio") from exc

        if _normalizar_header(header) != CABECALHO_ESPERADO:
            raise CabecalhoInvalido(f"cabecalho invalido: {header}")

        linhas: list[dict[str, str]] = []
        for row in reader:
            if not row or all(not (c or "").strip() for c in row):
                continue
            while len(row) < 4:
                row.append("")
            linhas.append(
                {
                    "nome": row[0],
                    "email": row[1],
                    "cpf": row[2],
                    "telefone": row[3],
                }
            )
        return ResultadoLeitura(linhas=linhas)
