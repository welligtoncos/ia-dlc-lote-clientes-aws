# Code generation summary — unit-worker-validacao

## Criado
- `worker/` — pacote `lote-worker` + Dockerfile
- Validadores + PBT em `libs/`
- Serviço `worker` real no `docker-compose.yml`
- Docs: README + `docs/smoke-test-api.md` (ciclo completo)

## Testes
`pytest libs/tests api/tests worker/tests --import-mode=importlib` → **30 passed**
