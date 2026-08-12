from hypothesis import given, strategies as st

from lote_shared.storage.chave import montar_chave


@given(st.text(min_size=1, max_size=40).filter(lambda s: s.strip() != ""))
def test_ref_sem_scheme_nem_absoluto(nome: str):
    ref = montar_chave(nome.replace("\\", "/").lstrip("/"))
    assert ref
    assert not ref.startswith("s3://")
    assert not ref.startswith("/")
    assert "://" not in ref
    assert ref.startswith("lotes/")
