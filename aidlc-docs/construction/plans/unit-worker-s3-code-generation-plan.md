# Plano de Geração de Código — unit-worker-s3

**Status**: Parte 2 **EXECUTADA** — worker **15 passed** · api **14 passed**  
**Código**: `worker/` (brownfield)  
**Histórias**: US-AWS-03 · US-AWS-04  

---

## Contexto

| Item | Detalhe |
|---|---|
| Objetivo | Task dual `caminho` **ou** `bucket`+`chave`; CSV via `lote_shared` `abrir`; fail-fast keys se s3 |
| Fora | Terraform ECS/Secrets (unit-infra-aws) |

---

## Etapas

### Etapa 1 — Settings + bootstrap keys
- [x] Evoluir settings.py
- [x] Fail-fast se s3 sem keys
- [x] US-AWS-03 (SEC)

### Etapa 2 — Leitor CSV + storage
- [x] `ler_csv_clientes_de_bytes` + `carregar_csv_clientes`
- [x] Mapear ObjetoNaoEncontrado → ArquivoAusente
- [x] US-AWS-03 · US-AWS-04

### Etapa 3 — Processador
- [x] Dual kwargs + armazenamento injetável
- [x] Idempotência preservada

### Etapa 4 — Task Celery
- [x] Assinatura dual + log backend
- [x] Retry 60/120/240

### Etapa 5 — Testes
- [x] Dual kwargs / memória / settings / modo
- [x] pytest worker 15 · api 14

### Etapa 6 — Docs + `.env.example`
- [x] `.env.example`
- [x] code-generation-summary.md

### Etapa 7 — Verificação final
- [x] pytest verde

---

## Aprovação do plano

[Answer]: A
