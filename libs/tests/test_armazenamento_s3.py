import boto3
import pytest
from moto import mock_aws

from lote_shared.domain.excecoes import ErroArmazenamento, ObjetoNaoEncontrado
from lote_shared.storage.s3 import ArmazenamentoArquivoS3


@mock_aws
def test_s3_salvar_existe_abrir():
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="lote-dev")
    store = ArmazenamentoArquivoS3(
        bucket="lote-dev", region="us-east-1", client=client
    )
    ref = store.salvar("9_arq.csv", b"csv-data")
    assert ref == "lotes/9_arq.csv"
    assert store.existe(ref) is True
    assert store.abrir(ref) == b"csv-data"


@mock_aws
def test_s3_existe_false():
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="lote-dev")
    store = ArmazenamentoArquivoS3(bucket="lote-dev", client=client)
    assert store.existe("lotes/missing.csv") is False


@mock_aws
def test_s3_abrir_ausente():
    client = boto3.client("s3", region_name="us-east-1")
    client.create_bucket(Bucket="lote-dev")
    store = ArmazenamentoArquivoS3(bucket="lote-dev", client=client)
    with pytest.raises(ObjetoNaoEncontrado):
        store.abrir("lotes/missing.csv")


def test_s3_bucket_obrigatorio():
    with pytest.raises(ErroArmazenamento):
        ArmazenamentoArquivoS3(bucket="")
