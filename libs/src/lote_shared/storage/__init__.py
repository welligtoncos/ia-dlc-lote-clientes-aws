from __future__ import annotations

from lote_shared.storage.chave import montar_chave
from lote_shared.storage.factory import criar_armazenamento
from lote_shared.storage.local import ArmazenamentoArquivoLocal
from lote_shared.storage.s3 import ArmazenamentoArquivoS3

__all__ = [
    "ArmazenamentoArquivoLocal",
    "ArmazenamentoArquivoS3",
    "criar_armazenamento",
    "montar_chave",
]
