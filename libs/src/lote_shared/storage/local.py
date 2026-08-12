from __future__ import annotations

from pathlib import Path

from lote_shared.domain.excecoes import ErroArmazenamento, ObjetoNaoEncontrado
from lote_shared.storage.chave import PREFIXO_PADRAO, montar_chave


class ArmazenamentoArquivoLocal:
    def __init__(
        self,
        diretorio_base: str,
        prefixo: str = PREFIXO_PADRAO,
    ) -> None:
        if not diretorio_base:
            raise ErroArmazenamento("diretorio_base obrigatorio para backend fs")
        self._base = Path(diretorio_base)
        self._prefixo = prefixo
        self._base.mkdir(parents=True, exist_ok=True)

    def _path(self, ref: str) -> Path:
        return self._base / ref

    def salvar(self, nome_destino: str, conteudo: bytes) -> str:
        ref = montar_chave(nome_destino, self._prefixo)
        destino = self._path(ref)
        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(conteudo)
        except OSError as exc:
            raise ErroArmazenamento(str(exc)) from exc
        return ref

    def existe(self, caminho: str) -> bool:
        return self._path(caminho).is_file()

    def abrir(self, caminho: str) -> bytes:
        path = self._path(caminho)
        if not path.is_file():
            raise ObjetoNaoEncontrado(caminho)
        try:
            return path.read_bytes()
        except OSError as exc:
            raise ErroArmazenamento(str(exc)) from exc
