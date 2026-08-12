from __future__ import annotations

import csv
import io
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from lote_shared.domain.excecoes import ErroArmazenamento, ObjetoNaoEncontrado
from lote_shared.storage import criar_armazenamento
from lote_shared.validacao.validadores_cliente import CABECALHO_ESPERADO


class CabecalhoInvalido(Exception):
    pass


class ArquivoAusente(Exception):
    pass


class ModoTarefaInvalido(Exception):
    """kwargs ambíguos ou incompletos (fs xor s3)."""


@dataclass
class ResultadoLeitura:
    linhas: list[dict[str, str]]


class _PortaAbrir(Protocol):
    def abrir(self, caminho: str) -> bytes: ...


def _normalizar_header(celulas: list[str]) -> tuple[str, ...]:
    normalizadas = []
    for i, c in enumerate(celulas):
        valor = c.strip().lstrip("\ufeff") if i == 0 else c.strip()
        normalizadas.append(valor.lower())
    return tuple(normalizadas)


def ler_csv_clientes_de_bytes(conteudo: bytes) -> ResultadoLeitura:
    texto = conteudo.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(texto))
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


def ler_csv_via_abrir(armazenamento: _PortaAbrir, ref: str) -> ResultadoLeitura:
    try:
        conteudo = armazenamento.abrir(ref)
    except ObjetoNaoEncontrado as exc:
        raise ArquivoAusente(str(exc)) from exc
    except ErroArmazenamento as exc:
        raise ArquivoAusente(str(exc)) from exc
    return ler_csv_clientes_de_bytes(conteudo)


def ler_csv_clientes(caminho: str) -> ResultadoLeitura:
    """Compat: path absoluto ou relativo a STORAGE_LOCAL_DIR."""
    path = Path(caminho)
    if not path.is_absolute():
        base = os.getenv("STORAGE_LOCAL_DIR") or os.getenv("STORAGE_PATH") or "."
        path = Path(base) / caminho
    if not path.is_file():
        raise ArquivoAusente(caminho)
    return ler_csv_clientes_de_bytes(path.read_bytes())


def carregar_csv_clientes(
    *,
    caminho: str | None = None,
    bucket: str | None = None,
    chave: str | None = None,
    settings: Any | None = None,
    armazenamento: _PortaAbrir | None = None,
) -> ResultadoLeitura:
    """Resolve kwargs fs|s3 e lê CSV via storage ou path absoluto."""
    caminho_ok = bool(caminho)
    s3_ok = bool(bucket) and bool(chave)
    if caminho_ok and s3_ok:
        raise ModoTarefaInvalido("informe caminho OU bucket+chave, nao ambos")
    if not caminho_ok and not s3_ok:
        raise ModoTarefaInvalido("informe caminho (fs) ou bucket+chave (s3)")

    if caminho_ok:
        path = Path(caminho)  # type: ignore[arg-type]
        if path.is_absolute():
            return ler_csv_clientes(caminho)  # type: ignore[arg-type]
        if armazenamento is not None:
            return ler_csv_via_abrir(armazenamento, caminho)  # type: ignore[arg-type]
        if settings is None:
            return ler_csv_clientes(caminho)  # type: ignore[arg-type]
        armaz = criar_armazenamento(
            "fs",
            diretorio_base=settings.diretorio_storage,
            prefixo=getattr(settings, "s3_prefix", "lotes/") or "lotes/",
        )
        return ler_csv_via_abrir(armaz, caminho)  # type: ignore[arg-type]

    # modo s3
    if armazenamento is not None:
        return ler_csv_via_abrir(armazenamento, chave)  # type: ignore[arg-type]
    if settings is None:
        raise ModoTarefaInvalido("settings obrigatorio para modo s3")
    armaz = criar_armazenamento(
        "s3",
        bucket=bucket or settings.s3_bucket,
        region=settings.aws_region,
        prefixo=settings.s3_prefix or "lotes/",
    )
    return ler_csv_via_abrir(armaz, chave)  # type: ignore[arg-type]
