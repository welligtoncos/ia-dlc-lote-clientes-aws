# Unidades de Trabalho — Fase 2 Migração AWS

**Decisões**: Q1=A · Q2=A · Q3=A · Q4=A · Q5=A · Q6=A · Q7=A · Q8=A · Q9=A  
**Plano**: `plans/fase2-aws-unit-of-work-plan.md`

---

## Visão geral

| Unidade | Pacote / área | Bounded context | Ownership | Deploy |
|---|---|---|---|---|
| `unit-libs-storage` | `libs/` (`lote-shared`) | Storage Portability | Mesmo time (Q3=A) | Lib (sem imagem) |
| `unit-api-cloud` | `api/` (`lote-api`) | Gestão de Lotes cloud | Mesmo time | Imagem ECR `api` |
| `unit-worker-s3` | `worker/` (`lote-worker`) | Validação cloud | Mesmo time | Imagem ECR `worker` |
| `unit-infra-aws` | `infra/terraform` + GHA + docs | Platform AWS | Mesmo time | Terraform state `dev` + workflow |

**Ordem Construction (Q6=A):**  
1. `unit-libs-storage` → 2. `unit-api-cloud` → 3. `unit-worker-s3` → 4. `unit-infra-aws`

**Regra Fase 1 preservada:** api ↔ worker sem import cruzado; ambos dependem de `lote-shared`.

---

## U1 — `unit-libs-storage`

### Responsabilidades
- `ArmazenamentoArquivoS3` + factory `criar_armazenamento(STORAGE_BACKEND)`
- Manter `ArmazenamentoArquivoLocal` e porta estável (ref opaca)
- Testes unitários + PBT relevantes do contrato de storage

### Não inclui
- Rotas HTTP, task Celery, Terraform

### Entregáveis
- Código em `libs/`; bump consumível por api/worker
- Testes da lib (incl. moto/fake S3 se aplicável)

### Histórias
US-AWS-02 (contrato storage), US-AWS-04 (fs continua disponível)

---

## U2 — `unit-api-cloud`

### Responsabilidades
- Composition root: factory storage por env
- Enqueue via AdaptadorCelery com payload `{lote_id, ref}`; tradução kwargs na infra do adapter
- Garantir Compose/`fs` e path cloud sem mudar contrato HTTP `/lotes`
- Smoke local regressão

### Não inclui
- Implementação S3 SDK (fica na lib); execução da task; Terraform/API Gateway

### Entregáveis
- Mudanças em `api/`; Dockerfile inalterado em essência
- Testes de casos de uso / enqueue

### Histórias
US-AWS-01 (consumo via Gateway — app ready), US-AWS-02, US-AWS-04

---

## U3 — `unit-worker-s3`

### Responsabilidades
- Task `ingerir_clientes` aceitando `{lote_id, bucket, chave}` e `{lote_id, caminho}`
- Ler CSV do S3 ou filesystem; validação + update RDS/MySQL
- Bootstrap worker com mesma factory storage se necessário

### Não inclui
- HTTP; mudanças em `libs/` sem coordenação; Terraform

### Entregáveis
- Mudanças em `worker/`; testes da task dual-backend

### Histórias
US-AWS-03

---

## U4 — `unit-infra-aws`

### Responsabilidades
- Terraform `dev` us-east-1: VPC/SG, RDS, S3, ElastiCache, ECR, ECS api+worker, ALB, API Gateway + API Key, IAM, secrets, logs
- GitHub Actions: build/push + `terraform apply` em `dev`
- Docs: dump/restore, rollback note, smoke cloud
- Controles Security Baseline (S3 privado, RDS privado, TLS, least-privilege) e change management leve

### Não inclui
- Lógica de validação de linha / regras de domínio

### Entregáveis
- `infra/terraform/**`, workflows GHA, runbooks em `docs/` ou `infra/`

### Histórias
US-AWS-01 (edge Gateway), US-AWS-05, US-AWS-06, US-AWS-07, US-AWS-08

---

## Estratégia de código (brownfield)

Monorepo existente mantido. Novos módulos sob `libs/`, deltas em `api/` e `worker/`, IaC sob `infra/terraform/`.
