from __future__ import annotations

import io
from typing import Any

from botocore.exceptions import ClientError

from lote_shared.domain.excecoes import ErroArmazenamento, ObjetoNaoEncontrado
from lote_shared.storage.chave import PREFIXO_PADRAO, montar_chave


class ArmazenamentoArquivoS3:
    def __init__(
        self,
        bucket: str,
        region: str | None = None,
        prefixo: str = PREFIXO_PADRAO,
        client: Any | None = None,
    ) -> None:
        if not bucket:
            raise ErroArmazenamento("S3_BUCKET obrigatorio para backend s3")
        self._bucket = bucket
        self._prefixo = prefixo
        if client is not None:
            self._client = client
        else:
            import boto3

            kwargs = {}
            if region:
                kwargs["region_name"] = region
            self._client = boto3.client("s3", **kwargs)

    def salvar(self, nome_destino: str, conteudo: bytes) -> str:
        ref = montar_chave(nome_destino, self._prefixo)
        try:
            self._client.upload_fileobj(
                io.BytesIO(conteudo),
                self._bucket,
                ref,
            )
        except ClientError as exc:
            raise ErroArmazenamento(str(exc)) from exc
        return ref

    def existe(self, caminho: str) -> bool:
        try:
            self._client.head_object(Bucket=self._bucket, Key=caminho)
            return True
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {"404", "NoSuchKey", "NotFound", "404 Not Found"}:
                return False
            raise ErroArmazenamento(str(exc)) from exc

    def abrir(self, caminho: str) -> bytes:
        buffer = io.BytesIO()
        try:
            self._client.download_fileobj(self._bucket, caminho, buffer)
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {"404", "NoSuchKey", "NotFound", "404 Not Found"}:
                raise ObjetoNaoEncontrado(caminho) from exc
            raise ErroArmazenamento(str(exc)) from exc
        return buffer.getvalue()
