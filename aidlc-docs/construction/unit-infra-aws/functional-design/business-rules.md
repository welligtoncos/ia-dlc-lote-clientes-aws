# Regras de Negócio (Plataforma) — unit-infra-aws

## RN-STACK — Escopo (Q1=A)

| ID | Regra |
|---|---|
| RN-S01 | Ambiente único `dev` em `us-east-1`, single-AZ |
| RN-S02 | Recursos: VPC/SG, RDS MySQL, S3, ElastiCache, ECR, ECS api+worker, ALB, API Gateway + API Key, IAM, Secrets, CloudWatch Logs |
| RN-S03 | Código em módulos sob `infra/terraform/` + root `envs/dev` |

## RN-EDGE — API Key (Q3=A, US-AWS-01)

| ID | Regra |
|---|---|
| RN-E01 | API Key criada/gerenciada pelo Terraform |
| RN-E02 | Valor da key **não** commitado; output sensível e/ou Secrets Manager |
| RN-E03 | Cliente autentica com header `x-api-key`; FastAPI **não** valida a key |

## RN-SEC — Secrets e baseline (Q4=A, Q6=A, US-AWS-08)

| ID | Regra |
|---|---|
| RN-C01 | DB password, AWS keys app, API Key value via Secrets Manager / SSM SecureString |
| RN-C02 | Task defs ECS injetam secrets como env; placeholders TF; valores fora do git |
| RN-C03 | S3: block public access + bucket privado; prefixo `lotes/` |
| RN-C04 | RDS e ElastiCache apenas em subnets privadas |
| RN-C05 | IAM least-privilege (api: Put/Head S3; worker: Get/Head S3; ambos: RDS/cache conforme necessidade) |
| RN-C06 | TLS no edge (API Gateway HTTPS) |

## RN-OPS — Change, dump, rollback (Q5=A, Q6=A)

| ID | Regra |
|---|---|
| RN-O01 | Mudanças TF/GHA só via PR + merge |
| RN-O02 | `terraform apply` automático só `dev` via GHA após merge |
| RN-O03 | Runbook dump/restore RDS com `mysqldump` (manual/doc; sem automação GHA completa neste ciclo) |
| RN-O04 | Nota de rollback: re-apply TF anterior e/ou redeploy tag ECR anterior |
| RN-O05 | Smoke checklist pós-deploy (health Gateway/API, enqueue smoke opcional) |

## Mapeamento

| US | Regras |
|---|---|
| US-AWS-01 | RN-E* |
| US-AWS-05 | RN-S*, RN-O01–O02, RN-O05 |
| US-AWS-06 | RN-O03 |
| US-AWS-07 | RN-O01, RN-O04 |
| US-AWS-08 | RN-C* |
