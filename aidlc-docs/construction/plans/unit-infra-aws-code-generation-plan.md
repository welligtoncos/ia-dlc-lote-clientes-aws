# Plano de Geração de Código — unit-infra-aws

**Status**: Parte 2 **EXECUTADA**  
**Código**: `infra/terraform/**`, `.github/workflows/deploy-dev.yml`, `infra/docs/**`  
**Histórias**: US-AWS-01 · US-AWS-05 · US-AWS-06 · US-AWS-07 · US-AWS-08  

---

## Etapas

### Etapa 1 — Estrutura Terraform root + backend
- [x] `envs/dev` + backend comentado + bootstrap doc

### Etapa 2 — Módulo `network`
- [x] VPC, subnets, SGs (2 AZs p/ ALB)

### Etapa 3 — Módulos `data` + `storage`
- [x] RDS MySQL + ElastiCache + S3 SSE

### Etapa 4 — Módulos `security` + `observability`
- [x] IAM + Secrets placeholder + CW logs

### Etapa 5 — Módulos `compute` + `edge`
- [x] ECR/ECS/ALB + HTTP API + API key secret

### Etapa 6 — Wire root + README
- [x] `envs/dev/main.tf` + `infra/README.md`

### Etapa 7 — GitHub Actions
- [x] `deploy-dev.yml`

### Etapa 8 — Runbooks
- [x] smoke / dump-restore / rollback / bootstrap

### Etapa 9 — Summary + verificação
- [x] code-generation-summary.md
- [x] `terraform fmt` ok; `validate` bloqueado por disco (provider AWS)

---

## Aprovação do plano

[Answer]: A
