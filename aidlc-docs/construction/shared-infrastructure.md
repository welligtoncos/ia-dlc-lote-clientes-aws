# Infraestrutura Compartilhada

**Referenciado por**: unit-dominio-api · unit-worker-validacao · **unit-libs-storage** · **unit-api-cloud** · **unit-worker-s3** · **unit-infra-aws**  
**Orquestração local**: **um** `docker-compose.yml` na **raiz** do monorepo  
**Projetos Python**: separados (`api/`, `worker/`, `libs/`)  
**IaC cloud**: `infra/terraform/envs/dev` (unit-infra-aws)

---

## Recursos compartilhados (MVP local)

| Recurso | Spec | Consumidores |
|---|---|---|
| MySQL 8 | DB `lote`, user/senha via env | api, worker |
| Valkey | `:6379` — **DB 0** broker Celery; **DB 1** cache GET + invalidação | api (broker+cache), worker (broker + **invalidação cache**) |
| Volume `lotes_files` | path container `/data/lotes` | api (write), worker (read); mount RW |
| Rede Compose | bridge default / `lote-net` | todos |

---

## Contratos de conexão (local)

| Uso | URL / path |
|---|---|
| SQLAlchemy | `mysql+pymysql://...@mysql:3306/lote` |
| Celery broker | `redis://valkey:6379/0` |
| Cache | `redis://valkey:6379/1` |
| Arquivos (fs) | `STORAGE_LOCAL_DIR` default `/data/lotes` |

---

## Contrato de storage Fase 2 (unit-libs-storage)

| Variável | Default | Notas |
|---|---|---|
| `STORAGE_BACKEND` | `fs` | `fs` \| `s3` |
| `STORAGE_LOCAL_DIR` | `/data` | Compose (volume em `/data`; chaves `lotes/...`) |
| `S3_BUCKET` | — | Obrigatório se `s3` |
| `AWS_REGION` | `us-east-1` | |
| `S3_PREFIX` | `lotes/` | Chaves relativas |
| `AWS_ACCESS_KEY_ID` | — | **Obrigatório se `s3`** na **API** e no **worker** (api Q6=B; worker Q6=A) |
| `AWS_SECRET_ACCESS_KEY` | — | Pair da access key |

- Ref opaca = chave relativa (ex. `lotes/12_arq.csv`), nunca path absoluto/`s3://`
- Bucket + IAM (`Put/Get/Head` em `lotes/*`) → provisionados em **unit-infra-aws**
- Pacote `lote-shared`: path local **e** publicação **CodeArtifact**
- API com `STORAGE_BACKEND=s3` enfileira `{lote_id, bucket, chave}`; com `fs` enfileira `{lote_id, caminho}`
- Worker consome dual kwargs; lê via `abrir`; fail-fast se s3 sem keys

---

## Contrato AWS `dev` (unit-infra-aws)

| Recurso | Spec |
|---|---|
| Região / AZ | `us-east-1` · single-AZ |
| Tags | `Project=lote-clientes`, `Env=dev` |
| VPC | /16 · 1 public · private-app · private-data |
| RDS | MySQL 8 single-AZ · privado |
| ElastiCache | Redis/Valkey single-node · privado |
| S3 | privado · SSE-S3 · prefixo `lotes/` |
| Compute | ECS Fargate api+worker desired=1 · ECR |
| Edge | API Gateway + API Key → ALB privado → api `/health` |
| Secrets | Secrets Manager → env ECS |
| State TF | S3 + lock · apply via GHA OIDC pós-merge |
| Runbooks | `infra/docs/` smoke · dump-restore · rollback |

Paridade local ↔ cloud:

| Local (Compose) | Cloud `dev` |
|---|---|
| MySQL container | RDS MySQL |
| Valkey | ElastiCache |
| Volume `/data` | S3 `lotes/` |
| api:8000 | Gateway URL + `x-api-key` |
| worker | ECS worker (sem porta) |

---

## Serviços de aplicação

| Serviço | Imagem | Portas host | Notas |
|---|---|---|---|
| `api` | `api/Dockerfile` | 8000:8000 | Uvicorn |
| `worker` | `worker/Dockerfile` | **nenhuma** | Celery |

---

## Regras

1. Não duplicar MySQL/Valkey/volume em composes por projeto.
2. Api e worker **devem** montar o mesmo volume nomeado quando `STORAGE_BACKEND=fs`.
3. Worker sobe por padrão.
4. Mudanças neste arquivo exigem alinhamento das unidades consumidoras.
5. Contratos AWS detalhados acima (seção unit-infra-aws) e em `aidlc-docs/construction/unit-infra-aws/infrastructure-design/`.

---

## Arquivos na raiz

```text
docker-compose.yml
.env.example
infra/README.md
infra/terraform/
infra/docs/
.github/workflows/
api/Dockerfile
worker/Dockerfile
libs/
```
