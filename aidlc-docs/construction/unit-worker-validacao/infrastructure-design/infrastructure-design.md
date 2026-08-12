# Design de Infraestrutura — unit-worker-validacao

**Decisões**: Q1–Q7 = A

---

## Escopo

| Ambiente | Neste ciclo |
|---|---|
| Local | **Sim** — serviço `worker` no `docker-compose.yml` da **raiz** (substitui placeholder) |
| AWS | **Não provisionar**; esboço já em `infra/README.md` |

Projeto Python: `worker/` (`lote-worker`) com `Dockerfile` próprio.

---

## Mapeamento lógico → infra local

| Componente lógico | Infra local |
|---|---|
| CeleryApp / TaskIngerirClientes | Serviço Compose `worker` — build `worker/Dockerfile` |
| Comando | `celery -A lote_worker.celery_app worker --loglevel=INFO --concurrency=2` |
| LoteRepo / MySQL | Serviço `mysql:8` compartilhado |
| LeitorCsv / arquivos | Volume `lotes_files` → `/data/lotes` (RW no volume; worker lê) |
| Broker | Valkey DB **0** (`CELERY_BROKER_URL`) |
| CacheInvalidator | Valkey DB **1** (`CACHE_URL`) |
| JsonLogger | stdout JSON → `docker compose logs worker` |
| Rede | Só rede interna compose — **sem** portas publicadas |

Detalhes compartilhados: [`../../shared-infrastructure.md`](../../shared-infrastructure.md).

---

## Variáveis de ambiente (worker)

| Variável | Exemplo local |
|---|---|
| `DATABASE_URL` | `mysql+pymysql://lote:lote@mysql:3306/lote` |
| `CELERY_BROKER_URL` | `redis://valkey:6379/0` |
| `CACHE_URL` | `redis://valkey:6379/1` |
| `STORAGE_PATH` | `/data/lotes` |
| `LOG_LEVEL` | `INFO` |

Fail-fast na startup se `DATABASE_URL` / `CELERY_BROKER_URL` / `STORAGE_PATH` ausentes.

Celery runtime (código/config app):
- `task_acks_late=True`
- `worker_prefetch_multiplier=1`
- sem result backend
- autoretry 3× (60/120/240s) na task

---

## Serviço Compose `worker` (especificação)

```yaml
# trecho-alvo (Code Generation)
worker:
  build:
    context: .
    dockerfile: worker/Dockerfile
  command: celery -A lote_worker.celery_app worker --loglevel=INFO --concurrency=2
  environment:
    DATABASE_URL: mysql+pymysql://lote:lote@mysql:3306/lote
    CELERY_BROKER_URL: redis://valkey:6379/0
    CACHE_URL: redis://valkey:6379/1
    STORAGE_PATH: /data/lotes
    LOG_LEVEL: INFO
  volumes:
    - lotes_files:/data/lotes
  depends_on:
    mysql:
      condition: service_healthy
    valkey:
      condition: service_started
```

Sem `ports:`.

---

## Esboço AWS futuro (não aplicar)

| Local | AWS (Fase 2) |
|---|---|
| serviço `worker` | ECS Fargate service (worker) |
| imagem `worker` | ECR |
| Valkey | ElastiCache |
| MySQL | RDS |
| volume | EFS (ou S3) |

---

## Alteração no compose existente

Remover o placeholder `profiles: ["worker-real"]` / imagem Valkey falsa; serviço `worker` sobe por padrão com `api`, `mysql`, `valkey`.
