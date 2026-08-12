# Componentes Lógicos — unit-infra-aws

**Decisão Q5=A**: módulos compostos pelo root `envs/dev`.

---

```text
envs/dev (root)
  |
  +-- network        VPC, subnets, SGs base
  +-- data           RDS MySQL + ElastiCache
  +-- storage        S3 lotes (privado, SSE)
  +-- compute        ECR + ECS api/worker + ALB
  +-- edge           API Gateway + API Key → ALB
  +-- security       IAM roles/policies + Secrets placeholders
  +-- observability  CloudWatch log groups
```

## Por módulo

| Módulo | Responsabilidade |
|---|---|
| `network` | VPC single-AZ, public/private subnets, NAT se necessário |
| `data` | RDS + ElastiCache (privados); outputs endpoints |
| `storage` | Bucket S3 + block public + SSE-S3 |
| `compute` | ECR repos, task defs, services desired=1, ALB+TG `/health` |
| `edge` | HTTP API / REST API + usage plan + API Key |
| `security` | Task roles (S3 Put/Get), execution role, secrets refs |
| `observability` | Log groups api/worker |

## Integração app (contrato)

| Serviço | Env injetado (via secrets/vars) |
|---|---|
| api | `DATABASE_URL`, broker/cache, `STORAGE_BACKEND=s3`, bucket, AWS keys, region |
| worker | Idem + concurrency implícita na command |

## Fora dos módulos TF (mas nesta unit)

| Artefato | Papel |
|---|---|
| `.github/workflows` | build/push + terraform apply |
| Runbooks | dump/restore, rollback, smoke |
