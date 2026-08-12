# Estrutura de Código

## Organização do Monorepo

```text
ia-dlc-lote-clientes-aws/
├── api/                 # lote-api
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── src/lote_api/
│   │   ├── presentation/   # FastAPI
│   │   ├── application/    # casos de uso
│   │   └── infrastructure/ # Celery client, storage local, settings
│   └── tests/
├── worker/              # lote-worker
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── src/lote_worker/
│   │   ├── tasks/ingerir_clientes.py
│   │   ├── application/processador.py
│   │   └── infrastructure/ # leitor CSV, cache invalidator
│   └── tests/
├── libs/                # lote-shared
│   ├── pyproject.toml
│   ├── src/lote_shared/
│   │   ├── domain/
│   │   ├── ports/
│   │   ├── persistence/
│   │   ├── cache/
│   │   └── validacao/
│   └── tests/
├── migrations/001_lotes.sql
├── docker-compose.yml
├── fixtures/
├── docs/
└── infra/               # esboço AWS (sem Terraform ainda)
```

## Padrões

- Hexagonal: domain/ports em `lote-shared`; adapters em api/worker
- Isolamento: **proibido** import `lote_api` ↔ `lote_worker`
- Idioma: identificadores em português

## Pontos de atenção para migração AWS

- `ArmazenamentoArquivoLocal` (filesystem) → precisa adapter **S3**
- Payload task usa `caminho` local → evoluir para chave S3
- Settings via env já portáveis (`DATABASE_URL`, `CELERY_BROKER_URL`, `CACHE_URL`)
