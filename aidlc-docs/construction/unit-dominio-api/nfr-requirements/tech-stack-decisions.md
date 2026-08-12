# Decisões de Stack — unit-dominio-api

**Decisão Q5=A** — alinhada ao PRD.

## Runtime e linguagem

| Escolha | Versão / nota |
|---|---|
| Linguagem | Python **3.12+** |
| Empacotamento | Projetos `lote-api` e `lote-shared` com `pyproject.toml` separados |

## API HTTP

| Escolha | Justificativa |
|---|---|
| FastAPI | OpenAPI automático, tipagem, async-ready |
| Uvicorn | ASGI padrão para FastAPI |
| Pydantic v2 | Validação de DTOs de request/response |

## Persistência

| Escolha | Justificativa |
|---|---|
| SQLAlchemy 2.x | ORM moderno, alinhado ao PRD |
| PyMySQL | Driver MySQL puro-Python |
| MySQL 8 | Banco do compose / futuro RDS |

## Mensageria (cliente)

| Escolha | Justificativa |
|---|---|
| Celery (client/`send_task` ou `apply_async`) | Enqueue only; worker em projeto separado |
| Broker Valkey (`redis://`) | Protocolo Redis |

## Logging

| Escolha | Justificativa |
|---|---|
| Logs JSON em stdout | NFR-OBS-01; coleta via Docker logs |

## Testes

| Escolha | Justificativa |
|---|---|
| pytest | Padrão Python |
| Hypothesis (ou equivalente PBT) | P-API-* (NFR-TEST-02) |
| httpx / Starlette TestClient | NFR-TEST-03 |

## O que não usar neste ciclo (API)

| Item | Motivo |
|---|---|
| SQLModel | Não escolhido (Q5=A = SQLAlchemy) |
| Prometheus client | Q6=A |
| Auth middleware | Fora de escopo / Q4=A |
| pandas | Parsing CSV fica no **worker** |

## Dependências entre projetos

```text
lote-api  -->  lote-shared  -->  (SQLAlchemy/PyMySQL para persistence compartilhada)
lote-api  -->  celery[redis] (cliente)
lote-api  -->  fastapi, uvicorn, pydantic
```

## Variáveis de ambiente (mínimo)

| Variável | Uso |
|---|---|
| `DATABASE_URL` | MySQL |
| `CELERY_BROKER_URL` | Valkey |
| `STORAGE_PATH` | Volume compartilhado |
| `LOG_LEVEL` | Nível de log |

Valores concretos e compose → Infrastructure Design.
