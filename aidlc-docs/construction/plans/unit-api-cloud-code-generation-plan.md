# Plano de Geração de Código — unit-api-cloud

**Status**: Parte 2 **EXECUTADA** — api **14 passed**

## Etapas

### Etapa 1 — AdaptadorCelery dual kwargs
- [x] Evoluir adapters.py
- [x] Erro se s3 sem bucket
- [x] US-AWS-02

### Etapa 2 — Casos de uso payload mínimo
- [x] Ingerir / Reprocessar com `ref`
- [x] US-AWS-02, US-AWS-04

### Etapa 3 — Wiring main + settings
- [x] Passar backend/bucket ao AdaptadorCelery
- [x] Validar AWS keys se s3 (Q6=B)

### Etapa 4 — Testes
- [x] test_adaptador_celery_kwargs.py
- [x] pytest api 14 passed

### Etapa 5 — Docs + .env.example
- [x] code-generation-summary.md
- [x] .env.example

### Etapa 6 — Verificação
- [x] pytest verde
