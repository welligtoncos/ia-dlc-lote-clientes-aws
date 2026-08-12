# Design de Infraestrutura — unit-infra-aws

**Decisões**: Q1–Q7 = A

---

## Ambiente

| Item | Valor |
|---|---|
| Conta | Única `dev` |
| Região | `us-east-1` |
| AZ | single |
| Naming | `lote-*` |
| Tags | `Project=lote-clientes`, `Env=dev` |

---

## Mapeamento de serviços

| Necessidade | Serviço AWS | Notas |
|---|---|---|
| Rede | VPC /16, 1 public + 2 private (app, data) | SGs por tier |
| DB | RDS MySQL 8 single-AZ | privado |
| Broker/cache | ElastiCache Redis/Valkey single-node | DB0/DB1 lógico via URL |
| Arquivos | S3 privado + SSE-S3 | prefixo `lotes/` |
| Imagens | ECR `lote-api`, `lote-worker` | |
| Compute | ECS Fargate desired=1 cada | privado |
| LB | ALB privado | TG health `/health` |
| Edge | API Gateway + API Key | TLS; `x-api-key` |
| Secrets | Secrets Manager | DB, AWS keys, API key value |
| Logs | CloudWatch Logs | api/worker |
| State TF | S3 + lock | remoto |
| CI | GitHub Actions OIDC | build/push + apply |

---

## Layout Terraform

```text
infra/terraform/
  modules/
    network/
    data/           # rds + elasticache
    storage/        # s3
    compute/        # ecr + ecs + alb
    edge/           # apigw + api key
    security/       # iam + secrets refs
    observability/  # log groups
  envs/dev/
    backend.tf
    providers.tf
    main.tf
    variables.tf
    outputs.tf
    terraform.tfvars.example
```

---

## GHA (Q5=A)

| Trigger | Ações |
|---|---|
| push `main` (paths relevantes) | build/push ECR api+worker → `terraform apply` `envs/dev` |
| Auth | OIDC → role AWS (preferido) |

---

## Runbooks (Q6=A)

| Path | Conteúdo |
|---|---|
| `infra/docs/smoke-cloud.md` | Checklist pós-deploy |
| `infra/docs/dump-restore-rds.md` | mysqldump / restore |
| `infra/docs/rollback.md` | TF previous + tag ECR |
| `infra/README.md` | Visão geral + links |

---

## Outputs esperados

| Output | Uso |
|---|---|
| `api_gateway_url` | Cliente HTTP |
| `api_key_secret_arn` / instr. | Obter `x-api-key` (não printar em logs CI) |
| `s3_bucket` | Env app |
| `rds_endpoint` / secret | `DATABASE_URL` |
| `redis_endpoint` | broker/cache URLs |
| `ecr_api_url` / `ecr_worker_url` | GHA push |
