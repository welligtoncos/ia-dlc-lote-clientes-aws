from __future__ import annotations

import pytest

from lote_worker.settings import Settings


def test_settings_s3_exige_keys(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    cfg = Settings(
        database_url="mysql+pymysql://u:p@localhost/db",
        celery_broker_url="redis://localhost:6379/0",
        storage_backend="s3",
        s3_bucket="bucket",
        aws_access_key_id="",
        aws_secret_access_key="",
    )
    with pytest.raises(RuntimeError, match="AWS_ACCESS_KEY_ID"):
        cfg.validar_obrigatorios()


def test_settings_s3_ok_com_keys():
    cfg = Settings(
        database_url="mysql+pymysql://u:p@localhost/db",
        celery_broker_url="redis://localhost:6379/0",
        storage_backend="s3",
        s3_bucket="bucket",
        aws_access_key_id="AKIA",
        aws_secret_access_key="secret",
    )
    cfg.validar_obrigatorios()
