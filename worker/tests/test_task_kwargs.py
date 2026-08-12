from lote_worker.tasks.ingerir_clientes import _modo_backend


def test_modo_fs():
    assert _modo_backend("lotes/1.csv", None, None) == "fs"


def test_modo_s3():
    assert _modo_backend(None, "bucket", "lotes/1.csv") == "s3"


def test_modo_invalido():
    assert _modo_backend(None, None, None) == "invalido"
    assert _modo_backend("x", "b", "c") == "invalido"
    assert _modo_backend(None, "b", None) == "invalido"
