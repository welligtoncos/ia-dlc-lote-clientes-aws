# Design de Infraestrutura — unit-worker-s3

**Decisões**: Q1–Q7 = A

---

## Papel

Serviço `lote-worker`: consome Celery → lê CSV via lib (`abrir`) → valida/persiste MySQL.  
Não provisiona ECS/ElastiCache/Secrets (unit-infra-aws); define **contrato** de env e implantação.

---

## Mapeamento

| Necessidade | Recurso | Onde |
|---|---|---|
| Runtime | Imagem Docker `worker` → Compose + ECS Fargate | Compose agora; TF depois |
| Compute `dev` | 1 task ECS worker; Compose `--concurrency=2` | unit-infra-aws + Compose |
| Persistência arquivos | fs volume ou S3 via lib (**leitura**) | shared + libs |
| Fila | Celery broker (Valkey/ElastiCache) | env |
| DB | MySQL/RDS | env |
| Rede | Somente privada (sem ALB) | unit-infra-aws |
| Logs | stdout → CloudWatch Logs | ECS |

---

## Variáveis de ambiente (Worker)

| Variável | Obrigatória | Notas |
|---|---|---|
| `DATABASE_URL` | sim | RDS/MySQL |
| `CELERY_BROKER_URL` | sim | Valkey/ElastiCache DB0 |
| `CACHE_URL` | recomendado | invalidação DB1 |
| `STORAGE_BACKEND` | não (default `fs`) | `fs` \| `s3` |
| `STORAGE_LOCAL_DIR` | se `fs` | Compose: `/data` |
| `S3_BUCKET` | se `s3` | fallback se kwargs sem bucket |
| `S3_PREFIX` | não | default `lotes/` |
| `AWS_REGION` | se `s3` | default `us-east-1` |
| **`AWS_ACCESS_KEY_ID`** | **se `s3` (Q6=A)** | GetObject via lib/boto3 |
| **`AWS_SECRET_ACCESS_KEY`** | **se `s3` (Q6=A)** | Pair da access key |
| `LOG_LEVEL` | não | |

> Em ECS, injetar keys via Secrets Manager → env da task (não commit).  
> Code Generation desta unit: fail-fast se `STORAGE_BACKEND=s3` sem keys; atualizar `.env.example`.

---

## Rede (contrato)

```text
[AWS] Worker ECS (privado) -> ElastiCache / RDS / S3 (VPC ou endpoint)
[Compose] worker -> valkey / mysql / volume /data
Sem porta publicada no host.
```

## Explicitamente fora

Terraform recursos · Secrets Manager wiring · VPC endpoints → unit-infra-aws
