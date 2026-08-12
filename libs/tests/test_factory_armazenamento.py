from pathlib import Path

import boto3
import pytest
from moto import mock_aws

from lote_shared.domain.excecoes import ErroArmazenamento
from lote_shared.storage.factory import criar_armazenamento
from lote_shared.storage.local import ArmazenamentoArquivoLocal
from lote_shared.storage.s3 import ArmazenamentoArquivoS3


def test_factory_fs(tmp_path: Path):
    store = criar_armazenamento("fs", diretorio_base=str(tmp_path))
    assert isinstance(store, ArmazenamentoArquivoLocal)


def test_factory_default_fs(tmp_path: Path):
    store = criar_armazenamento(None, diretorio_base=str(tmp_path))
    assert isinstance(store, ArmazenamentoArquivoLocal)


@mock_aws
def test_factory_s3():
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="lote-dev-factory")
    store = criar_armazenamento("s3", bucket="lote-dev-factory", client=client)
    assert isinstance(store, ArmazenamentoArquivoS3)


def test_factory_invalido():
    with pytest.raises(ErroArmazenamento):
        criar_armazenamento("gcs", diretorio_base="/tmp")
