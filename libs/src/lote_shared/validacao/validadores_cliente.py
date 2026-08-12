"""Esboco de validadores de linha — detalhe fino na unit-worker-validacao."""


def validar_nome(valor: str | None) -> bool:
    return bool(valor and valor.strip())


def validar_email(valor: str | None) -> bool:
    if not valor or "@" not in valor:
        return False
    usuario, _, dominio = valor.partition("@")
    return bool(usuario) and "." in dominio


def validar_cpf(valor: str | None) -> bool:
    if not valor:
        return False
    digitos = "".join(c for c in valor if c.isdigit())
    return len(digitos) == 11


def validar_telefone(valor: str | None) -> bool:
    if valor is None or valor == "":
        return True
    digitos = "".join(c for c in valor if c.isdigit())
    return 10 <= len(digitos) <= 11
