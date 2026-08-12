from __future__ import annotations


PREFIXO_PADRAO = "lotes/"


def montar_chave(nome_destino: str, prefixo: str = PREFIXO_PADRAO) -> str:
    """Monta chave relativa opaca (sem scheme, sem path absoluto)."""
    nome = nome_destino.lstrip("/").replace("\\", "/")
    pref = prefixo or ""
    if pref and not pref.endswith("/"):
        pref = f"{pref}/"
    if pref and nome.startswith(pref):
        return nome
    return f"{pref}{nome}" if pref else nome
