# Servico de Ingestao de Clientes (MVP local)

Monorepo AI-DLC com projetos Python separados:

| Projeto | Pasta | Papel |
|---|---|---|
| lote-shared | `libs/` | dominio, portas, persistence, cache |
| lote-api | `api/` | FastAPI + enqueue Celery |
| lote-worker | `worker/` | (proxima unidade) |

## Subir API local

```bash
docker compose up -d --build mysql valkey api
curl http://localhost:8000/health
```

## Smoke test (manual)

Guia completo com respostas observadas: [`docs/smoke-test-api.md`](docs/smoke-test-api.md)

Resumo:

```bash
curl -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv"
curl http://localhost:8000/lotes
curl http://localhost:8000/lotes/1
curl -X DELETE http://localhost:8000/lotes/1
```

Fixture: `fixtures/clientes.csv`

> Sem worker, o lote permanece `PENDENTE` (contagens em 0). O `task_id` no POST indica enqueue no Valkey.

## Desenvolvimento

```bash
pip install -e ./libs -e "./api[dev]"
pytest libs/tests api/tests
```

## Documentacao AI-DLC

Ver `aidlc-docs/`.
