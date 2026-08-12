from __future__ import annotations

from typing import Any

from lote_shared.domain.excecoes import ErroArmazenamento
from lote_shared.storage.chave import PREFIXO_PADRAO
from lote_shared.storage.local import ArmazenamentoArquivoLocal
from lote_shared.storage.s3 import ArmazenamentoArquivoS3


def criar_armazenamento(
    backend: str | None = None,
    *,
    diretorio_base: str | None = None,
    bucket: str | None = None,
    region: str | None = None,
    prefixo: str = PREFIXO_PADRAO,
    client: Any | None = None,
) -> ArmazenamentoArquivoLocal | ArmazenamentoArquivoS3:
    """Factory fs|s3. Default: fs."""
    nome = (backend or "fs").strip().lower()
    if nome == "fs":
        if not diretorio_base:
            raise ErroArmazenamento(
                "STORAGE_LOCAL_DIR/diretorio_base obrigatorio para backend fs"
            )
        return ArmazenamentoArquivoLocal(diretorio_base, prefixo=prefixo)
    if nome == "s3":
        return ArmazenamentoArquivoS3(
            bucket=bucket or "",
            region=region,
            prefixo=prefixo,
            client=client,
        )
    raise ErroArmazenamento(f"STORAGE_BACKEND invalido: {backend!r}")
