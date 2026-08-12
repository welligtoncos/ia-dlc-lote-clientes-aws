# Validation summary — unit-worker-validacao

Validadores completos em `libs/src/lote_shared/validacao/validadores_cliente.py`:
- `validar_nome`, `validar_email`, `validar_cpf` (11 digitos + DV), `validar_telefone`
- `linha_valida`, `resumir_validacao` → `ResumoValidacao`

PBT: `libs/tests/test_validacao_pbt.py` (P-VAL-01..07; P-VAL-06 no worker).
