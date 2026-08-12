from unittest.mock import MagicMock, patch

import pytest

from lote_api.infrastructure.adapters import AdaptadorCelery


def test_kwargs_fs_com_ref():
    with patch("celery.Celery") as celery_cls:
        app = MagicMock()
        app.send_task.return_value = MagicMock(id="task-fs")
        celery_cls.return_value = app
        ad = AdaptadorCelery("redis://localhost:6379/0", storage_backend="fs")
        task_id = ad.executar(
            "ingerir_clientes", {"lote_id": 1, "ref": "lotes/1_a.csv"}
        )
    assert task_id == "task-fs"
    app.send_task.assert_called_once_with(
        "ingerir_clientes",
        kwargs={"lote_id": 1, "caminho": "lotes/1_a.csv"},
    )


def test_kwargs_s3_com_ref():
    with patch("celery.Celery") as celery_cls:
        app = MagicMock()
        app.send_task.return_value = MagicMock(id="task-s3")
        celery_cls.return_value = app
        ad = AdaptadorCelery(
            "redis://localhost:6379/0",
            storage_backend="s3",
            s3_bucket="lote-dev",
        )
        ad.executar("ingerir_clientes", {"lote_id": 2, "ref": "lotes/2_b.csv"})
    app.send_task.assert_called_once_with(
        "ingerir_clientes",
        kwargs={
            "lote_id": 2,
            "bucket": "lote-dev",
            "chave": "lotes/2_b.csv",
        },
    )


def test_s3_sem_bucket_falha_no_init():
    with patch("celery.Celery"):
        with pytest.raises(ValueError, match="S3_BUCKET"):
            AdaptadorCelery(
                "redis://localhost:6379/0", storage_backend="s3", s3_bucket=""
            )
