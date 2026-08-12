# Arquitetura de Implantação — unit-worker-validacao (local)

## Topologia Compose (raiz)

```text
                    Host :8000
                         |
                         v
              +---------------------+
              |  api (lote-api)     |
              +----------+----------+
                         |
         +---------------+---------------+
         |               |               |
         v               v               v
   +-----------+   +-----------+   +-------------+
   | mysql:8   |   | valkey    |   | lotes_files |
   | healthy   |   | :6379     |   | /data/lotes |
   +-----+-----+   | db0+db1   |   +------+------+
         |         +-----+-----+          |
         |               |                |
         v               v                v
              +---------------------------+
              |  worker (lote-worker)     |
              |  celery ... --concurrency=2
              |  sem portas no host       |
              +---------------------------+
```

### Text alternative
API na porta 8000; worker sem portas; ambos usam MySQL, Valkey (broker DB0 + cache DB1) e volume lotes_files no mesmo compose.

---

## Serviços (foco worker)

| Serviço | Build | Ports | Mounts | Depende |
|---|---|---|---|---|
| worker | `worker/Dockerfile` | — | `lotes_files:/data/lotes` | mysql (healthy), valkey |
| mysql | mysql:8 | 3306 | dados | — |
| valkey | valkey/valkey:8 | 6379 | — | — |
| api | `api/Dockerfile` | 8000 | `lotes_files:/data/lotes` | mysql, valkey |

---

## Fluxo de deploy local (ciclo completo)

```text
1. docker compose up -d --build mysql valkey api worker
2. curl http://localhost:8000/health
3. POST /lotes com fixtures/clientes.csv
4. docker compose logs -f worker
5. GET /lotes/{id} até CONCLUIDO ou ERRO
```

---

## Observabilidade

- `docker compose logs -f worker`
- Sem Flower / Prometheus neste ciclo

---

## Limites MVP

- 1 container worker, concurrency=2
- Sem réplicas, sem LB, sem TLS
- Restart best-effort
