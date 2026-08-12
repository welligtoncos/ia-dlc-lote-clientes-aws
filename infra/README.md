# Infra AWS — Fase 2 (`unit-infra-aws`)

**Ambiente**: `dev` · `us-east-1` · tags `Project=lote-clientes` / `Env=dev`

## Layout

```text
infra/terraform/
  modules/   network data storage security observability compute edge
  envs/dev/  root compose
infra/docs/  bootstrap-state smoke-cloud dump-restore-rds rollback
```

## Premissas

- **ALB exige ≥2 AZs** (AWS): subnets public/app em 2 AZs; **RDS/ElastiCache multi_az=false** (data plane single-AZ).
- API Gateway **HTTP API** + VPC Link → ALB privado; API key gerada e guardada em Secrets Manager (`x-api-key`). Enforcement nativo REST usage-plan pode ser reforçado depois (authorizer/WAF).
- Secrets: `db_password` e AWS keys via tfvars/CI secrets — **nao commit**.

## Aplicar localmente

1. Ler `infra/docs/bootstrap-state.md`
2. `cp envs/dev/terraform.tfvars.example envs/dev/terraform.tfvars` e preencher
3. `cd infra/terraform/envs/dev && terraform init && terraform plan && terraform apply`
4. Smoke: `infra/docs/smoke-cloud.md`

## CI

`.github/workflows/deploy-dev.yml` — OIDC (`AWS_ROLE_ARN`) + secrets `TF_VAR_DB_PASSWORD`, keys opcionais.

## Runbooks

| Doc | Uso |
|---|---|
| [bootstrap-state.md](docs/bootstrap-state.md) | State remoto |
| [smoke-cloud.md](docs/smoke-cloud.md) | Pos-deploy |
| [dump-restore-rds.md](docs/dump-restore-rds.md) | US-AWS-06 |
| [rollback.md](docs/rollback.md) | US-AWS-07 |
