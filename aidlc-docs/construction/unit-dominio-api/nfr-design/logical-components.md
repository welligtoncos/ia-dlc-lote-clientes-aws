# Componentes Lógicos NFR — unit-dominio-api

Componentes **lógicos** (ainda não são serviços AWS/Docker concretos — isso vai em Infrastructure Design).

---

## Diagrama lógico

```text
                    +------------------+
  Cliente HTTP ---> | Presentation     |
                    | + Logging MW     |
                    | + /health        |
                    | + rotas /lotes   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Application      |
                    | casos de uso     |
                    +--------+---------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
   +-------------+   +--------------+   +---------------+
   | LoteRepo    |   | FileStore    |   | CeleryClient  |
   | (+ pool DB) |   | (volume)     |   | (degraded OK) |
   +------+------+   +--------------+   +-------+-------+
          |                                         |
          v                                         v
   +-------------+                          +---------------+
   | MySQL       |                          | Valkey broker |
   +-------------+                          +-------+-------+
                                                    |
                                            +-------v-------+
                                            | Valkey cache  |
                                            | (GET lotes)   |
                                            +---------------+

  Settings (env fail-fast) atravessa todos os adapters.
```

### Text alternative
Presentation com middleware de log e /health; Application; adapters Repo (MySQL pool), FileStore, CeleryClient degraded; Valkey para broker e cache GET; Settings fail-fast.

---

## Catálogo de componentes

| Componente | Responsabilidade NFR | Depende de |
|---|---|---|
| **RequestLoggingMiddleware** | Gera `request_id`, mede latência, logs JSON, header `X-Request-ID` | — |
| **Settings** | Carrega env; valida `DATABASE_URL`, `CELERY_BROKER_URL`, `STORAGE_PATH` no boot | env |
| **HealthController** | `GET /health` → 200 se processo up (checagem profunda de deps opcional/MVP simples) | — |
| **LoteRepository** | Acesso MySQL via pool SQLAlchemy | Settings, MySQL |
| **CacheLote** (port/adapter) | Cache-aside GET por id (e lista se aplicável); invalidação em writes | Valkey |
| **FileStorageLocal** | Write/stream e `existe` no path configurado | Settings, volume |
| **CeleryTaskAdapter** | Enqueue allowlisted; catch → log + task_id nulo | Valkey broker |
| **OpenAPI** | Documentação automática FastAPI | — |

---

## Integração cache ↔ casos de uso

| Operação | Cache |
|---|---|
| GET /lotes/{id} | GET cache → miss → MySQL → SET |
| GET /lotes | Opcional cache `lotes:lista`; invalidar em qualquer write |
| POST /lotes | Sem read-cache; invalidate lista |
| PUT reprocessar | Invalidate `lote:{id}` + lista |
| DELETE | Invalidate `lote:{id}` + lista |

---

## Fora destes componentes (outros estágios/unidades)

- Worker Celery / parse CSV → unit-worker
- RDS/ECS/ALB/API Gateway → fora do MVP local (Infrastructure só compose)
