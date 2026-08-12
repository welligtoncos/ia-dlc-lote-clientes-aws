# Plano de Geração de Código — unit-worker-validacao

**Status**: Parte 2 CONCLUIDA — aguardando aprovação do codigo  
**Testes**: 30 passed (`pytest libs/tests api/tests worker/tests`)

## Etapas de execução (Parte 2)

### Etapa 1 — Estrutura do projeto worker
- [x] `worker/pyproject.toml` + árvore `src/` / `tests/`

### Etapa 2 — lote-shared: validadores completos
- [x] CPF DV, email, nome, telefone, `resumir_validacao`

### Etapa 3 — Testes PBT P-VAL-*
- [x] `libs/tests/test_validacao_pbt.py` + P-VAL-06 em worker

### Etapa 4 — Resumo validação
- [x] validation-summary.md

### Etapa 5 — Settings + CeleryApp + logging
- [x] settings, celery_app, logging_json

### Etapa 6 — LeitorCsv + CacheInvalidator
- [x] leitor_csv.py, cache_invalidator.py

### Etapa 7 — Task `ingerir_clientes`
- [x] processador + task com retry 60/120/240

### Etapa 8 — Testes worker
- [x] test_leitor_csv + test_processador

### Etapa 9 — Resumo task
- [x] task-summary.md

### Etapa 10 — Dockerfile + compose + docs
- [x] worker/Dockerfile, compose real, README, smoke-test

### Etapa 11 — Resumo final + pytest
- [x] code-generation-summary.md · 30 passed

## Extensoes
| Extensao | Status |
|---|---|
| PBT | Compliant (P-VAL) |
| Security/Resiliency | N/A disabled |
