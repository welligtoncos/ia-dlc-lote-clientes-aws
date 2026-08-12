# Servico de Ingestao de Clientes (MVP local)

Monorepo AI-DLC com projetos Python separados:

| Projeto | Pasta | Papel |
|---|---|---|
| lote-shared | `libs/` | dominio, portas, persistence, cache, validacao |
| lote-api | `api/` | FastAPI + enqueue Celery |
| lote-worker | `worker/` | Celery worker + validacao CSV |

## Subir stack local

```bash
docker compose up -d --build
curl http://localhost:8000/health
```

## Smoke test (ciclo completo)

Guia: [`docs/smoke-test-api.md`](docs/smoke-test-api.md)

```bash
curl -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv"
docker compose logs -f worker
curl http://localhost:8000/lotes/1
```

Fixture: `fixtures/clientes.csv`

## Desenvolvimento

```bash
pip install -e ./libs -e "./api[dev]" -e "./worker[dev]"
pytest libs/tests api/tests worker/tests -v
```

## Documentacao AI-DLC

Ver `aidlc-docs/`.
