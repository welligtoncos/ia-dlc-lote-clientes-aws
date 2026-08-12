# Arquitetura de Implantação — unit-dominio-api (local)

## Topologia Compose (raiz do monorepo)

```text
                    Host :8000
                         |
                         v
              +---------------------+
              |  api (lote-api)     |
              |  Uvicorn x1         |
              |  /health, /lotes    |
              +----------+----------+
                         |
         +---------------+---------------+
         |               |               |
         v               v               v
   +-----------+   +-----------+   +-------------+
   | mysql:8   |   | valkey    |   | lotes_files |
   | :3306     |   | :6379     |   | volume      |
   +-----------+   | db0 broker|   +------+------+
                   | db1 cache |          |
                   +-----+-----+          |
                         |                |
                         v                v
              +---------------------+-----+
              |  worker (lote-worker)     |
              |  Celery worker            |
              +---------------------------+
```

### Text alternative
Host acessa api:8000. Api e worker compartilham mysql, valkey (db0 broker / db1 cache) e volume lotes_files. Worker no mesmo compose.

---

## Serviços Compose (resumo)

| Serviço | Build/Image | Ports | Mounts | Depende |
|---|---|---|---|---|
| api | `api/Dockerfile` | 8000:8000 | `lotes_files:/data/lotes` | mysql, valkey |
| worker | `worker/Dockerfile` | — | `lotes_files:/data/lotes` | mysql, valkey |
| mysql | mysql:8 | 3306 opcional | volume dados | — |
| valkey | valkey/valkey:latest | 6379 opcional | — | — |

Rede: bridge default do compose (`lote-net` nomeada recomendada).

---

## Fluxo de deploy local

```text
1. docker compose up -d mysql valkey
2. migrate / init schema
3. docker compose up -d api worker
4. curl http://localhost:8000/health
```

---

## Limites MVP

- Sem réplicas, sem LB, sem TLS, sem API Gateway
- Restart: política default / manual (best-effort)
- Observabilidade: `docker compose logs -f api`
