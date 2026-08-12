# Design de Infraestrutura — unit-dominio-api

**Decisões**: Q1=B · Q2=A · Q3=A · Q4=A · Q5=A · Q6=A · Q7 original=C **resolvido por CQ1=A** (compose raiz único)

---

## Escopo

| Ambiente | Neste ciclo |
|---|---|
| Local | **Sim** — Docker Compose na raiz do monorepo |
| AWS | **Não provisionar**; apenas **esboço** Terraform/Copilot documentado (Q1=B) |

Projetos Python (`lote-api`, `lote-worker`, `lote-shared`) permanecem separados; a **orquestração local** é um único `docker-compose.yml` na raiz.

---

## Mapeamento lógico → infra local

| Componente lógico | Infra local |
|---|---|
| lote-api (Uvicorn) | Serviço Compose `api` — build `api/Dockerfile`, porta **8000**, 1 worker |
| MySQL / LoteRepository | Serviço `mysql:8` + volume de dados MySQL |
| FileStorage | Volume nomeado **`lotes_files`** montado em api e worker |
| Celery broker | Serviço `valkey` — URL DB **0** |
| CacheLote (GET) | Mesmo `valkey` — URL DB **1** |
| Logs / health | stdout JSON + `GET /health` |
| Worker (outra unidade) | Serviço `worker` no **mesmo** compose (build `worker/Dockerfile`) |

Detalhes compartilhados: [`../shared-infrastructure.md`](../../shared-infrastructure.md) (caminho: `aidlc-docs/construction/shared-infrastructure.md`).

---

## Variáveis de ambiente (api)

| Variável | Exemplo local |
|---|---|
| `DATABASE_URL` | `mysql+pymysql://lote:lote@mysql:3306/lote` |
| `CELERY_BROKER_URL` | `redis://valkey:6379/0` |
| `CACHE_URL` | `redis://valkey:6379/1` |
| `STORAGE_PATH` | `/data/lotes` |
| `LOG_LEVEL` | `INFO`

Fail-fast na startup se `DATABASE_URL` / `CELERY_BROKER_URL` / `STORAGE_PATH` ausentes.

---

## Esboço AWS futuro (não aplicar neste ciclo)

| Local | AWS (Fase 2) |
|---|---|
| serviço `api` | ECS Fargate service |
| imagem `api` | ECR |
| `mysql` | RDS MySQL |
| `valkey` | ElastiCache Valkey |
| volume `lotes_files` | EFS (ou S3 em evolução) |
| porta 8000 | ALB → task; API Gateway opcional depois |
| secrets | Secrets Manager |

Documentar stub em `infra/README.md` ou `infra/terraform/` (esqueleto) na Code Generation — **sem `terraform apply`**.

---

## Init de schema

- Script SQL ou Alembic disparado no boot da api / job `migrate` no compose.
- Tabela `lotes` conforme requirements.
