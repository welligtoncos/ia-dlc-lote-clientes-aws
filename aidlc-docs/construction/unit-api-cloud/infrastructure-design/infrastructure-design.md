# Design de Infraestrutura — unit-api-cloud

**Decisões**: Q1=A · Q2=A · Q3=A · Q4=A · Q5=A · **Q6=B** · Q7=A

---

## Papel

Serviço HTTP `lote-api`: upload → storage (lib) → enqueue Celery.  
Não provisiona Gateway/ALB/ECS (unit-infra-aws); define **contrato** de env e implantação.

---

## Mapeamento

| Necessidade | Recurso | Onde |
|---|---|---|
| Runtime | Imagem Docker `api` → Compose + ECS Fargate | Compose agora; TF depois |
| Compute `dev` | 1 task ECS api | unit-infra-aws |
| Persistência arquivos | fs volume ou S3 via lib | shared + libs |
| Fila | Celery broker (Valkey/ElastiCache) | env |
| Edge | API Gateway → ALB → api | unit-infra-aws |
| Health | `GET /health` → target group ALB | app + TF |
| Logs | stdout → CloudWatch Logs | ECS |

---

## Variáveis de ambiente (API)

| Variável | Obrigatória | Notas |
|---|---|---|
| `DATABASE_URL` | sim | RDS/MySQL |
| `CELERY_BROKER_URL` | sim | Valkey/ElastiCache DB0 |
| `CACHE_URL` | recomendado | DB1 |
| `STORAGE_BACKEND` | não (default `fs`) | `fs` \| `s3` |
| `STORAGE_LOCAL_DIR` / `STORAGE_PATH` | se `fs` | Compose: `/data` |
| `S3_BUCKET` | se `s3` | |
| `S3_PREFIX` | não | default `lotes/` |
| `AWS_REGION` | se `s3` | default `us-east-1` |
| **`AWS_ACCESS_KEY_ID`** | **se `s3` (Q6=B)** | API faz PutObject via boto3 |
| **`AWS_SECRET_ACCESS_KEY`** | **se `s3` (Q6=B)** | Pair da access key |
| `LOG_LEVEL` | não | |

> Em ECS, preferir injetar keys via Secrets Manager → env da task (não commit).  
> Task role IAM continua desejável na infra; Q6=B exige presença das vars de access key quando `STORAGE_BACKEND=s3` neste ciclo.

---

## Rede (contrato)

```text
Internet -> API Gateway (API Key) -> ALB (privado) -> ECS api:8000
Compose: host:8000 -> api:8000
```

## Explicitamente fora

Terraform recursos · API Key creation · scaling policies → unit-infra-aws  
Consumo task `{bucket,chave}` → unit-worker-s3
