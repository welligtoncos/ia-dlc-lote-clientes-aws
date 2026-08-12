from hypothesis import given, strategies as st

from lote_shared.validacao.validadores_cliente import (
    linha_valida,
    resumir_validacao,
    validar_cpf,
    validar_email,
    validar_nome,
    validar_telefone,
)


def _cpf_com_dv(base9: str) -> str:
    soma = sum(int(base9[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10) % 11
    if d1 == 10:
        d1 = 0
    temp = base9 + str(d1)
    soma = sum(int(temp[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10) % 11
    if d2 == 10:
        d2 = 0
    return temp + str(d2)


@given(st.text(min_size=9, max_size=9).map(lambda s: "".join(c for c in s if c.isdigit())))
def test_p_val_01_cpf_dv_oraculo(digitos: str):
    if len(digitos) != 9 or digitos == digitos[0] * 9:
        assert validar_cpf(digitos) is False
        return
    cpf = _cpf_com_dv(digitos)
    assert validar_cpf(cpf) is True
    assert validar_cpf(cpf[:10]) is False
    assert validar_cpf(f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}") is False


def test_p_val_02_email_regras_basicas():
    assert validar_email("ana@ex.com") is True
    assert validar_email("sem-arroba") is False
    assert validar_email("a@b") is False
    assert validar_email(None) is False


@given(st.one_of(st.none(), st.just(""), st.from_regex(r"[0-9]{10,11}", fullmatch=True)))
def test_p_val_03_telefone(valor: str | None):
    assert validar_telefone(valor) is True


@given(st.from_regex(r"[0-9]{1,9}", fullmatch=True) | st.from_regex(r"[0-9]{12}", fullmatch=True))
def test_p_val_03_telefone_invalido_tamanho(valor: str):
    assert validar_telefone(valor) is False


@given(st.sampled_from(["", "   ", None]))
def test_p_val_04_nome_vazio(valor: str | None):
    assert validar_nome(valor) is False


@given(st.lists(st.booleans(), min_size=0, max_size=50))
def test_p_val_05_invariante_contagem(flags: list[bool]):
    linhas = []
    for ok in flags:
        if ok:
            linhas.append(
                {
                    "nome": "Ana",
                    "email": "ana@ex.com",
                    "cpf": "52998224725",
                    "telefone": "",
                }
            )
        else:
            linhas.append(
                {"nome": "", "email": "x", "cpf": "123", "telefone": "abc"}
            )
    resumo = resumir_validacao(linhas)
    assert resumo.total_linhas == resumo.linhas_validas + resumo.linhas_invalidas
    assert resumo.linhas_validas == sum(1 for f in flags if f)
    assert resumo.linhas_invalidas == sum(1 for f in flags if not f)


def test_p_val_07_cpf_mascarado_nunca_valido():
    assert validar_cpf("529.982.247-25") is False
    assert validar_cpf("52998224725") is True


def test_linha_valida_exemplo():
    assert linha_valida(
        {
            "nome": "Maria",
            "email": "m@ex.com",
            "cpf": "52998224725",
            "telefone": "11987654321",
        }
    )
