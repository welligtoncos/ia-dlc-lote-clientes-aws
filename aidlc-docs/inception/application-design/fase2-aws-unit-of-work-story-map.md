# Mapa Histórias → Unidades — Fase 2 AWS

| História | Prioridade | Unidade(s) | Notas |
|---|---|---|---|
| US-AWS-01 | Must | `unit-infra-aws` + `unit-api-cloud` | Gateway+Key (infra); API responde contrato (api) |
| US-AWS-02 | Must | `unit-libs-storage` + `unit-api-cloud` | S3 adapter (libs); upload+enqueue (api) |
| US-AWS-03 | Must | `unit-worker-s3` | Task lê S3 / atualiza RDS |
| US-AWS-04 | Must | `unit-libs-storage` + `unit-api-cloud` (+ worker regressão) | Compose `fs` |
| US-AWS-05 | Must | `unit-infra-aws` | Terraform + GHA apply + smoke |
| US-AWS-06 | Must | `unit-infra-aws` | Dump/restore docs |
| US-AWS-07 | Must | `unit-infra-aws` | Change mgmt leve (Q8=A) |
| US-AWS-08 | Must | `unit-infra-aws` | Security Baseline (Q8=A) |

## Cobertura

- Todas as US-AWS-01..08 atribuídas: **Sim**
- Nenhuma história órfã: **Sim**

## Por unidade (resumo)

| Unidade | Histórias |
|---|---|
| unit-libs-storage | US-AWS-02, US-AWS-04 |
| unit-api-cloud | US-AWS-01, US-AWS-02, US-AWS-04 |
| unit-worker-s3 | US-AWS-03, US-AWS-04 (regressão) |
| unit-infra-aws | US-AWS-01, US-AWS-05, US-AWS-06, US-AWS-07, US-AWS-08 |
