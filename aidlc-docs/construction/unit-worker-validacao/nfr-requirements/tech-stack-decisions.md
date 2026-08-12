# Decisões de Stack — unit-worker-validacao

**Decisão Q7=A** — alinhada ao PRD e ao isolamento de projetos.

## Runtime e linguagem

| Escolha | Versão / nota |
|---|---|
| Linguagem | Python **3.12+** |
| Empacotamento | Projeto `lote-worker` com `pyproject.toml` próprio |
| Dependência compartilhada | `lote-shared` (path/editable) |

## Worker / mensageria

| Escolha | Justificativa |
|---|---|
| Celery | Task `ingerir_clientes`, retry/backoff |
| Broker Valkey (`redis://`) | Mesmo broker da API (DB0) |
| Result backend | **Desabilitado** neste ciclo (Q7=A); verdade no MySQL |
| Concurrency | `concurrency=2` (Q2=B) |

## Parsing CSV

| Escolha | Justificativa |
|---|---|
| `csv` (stdlib) | Streaming linha a linha; sem pandas (Q3=A) |

## Persistência

| Escolha | Justificativa |
|---|---|
| SQLAlchemy 2.x via `lote-shared` | Mesmo repositório `LoteRepositorio` |
| PyMySQL / MySQL 8 | Alinhado à API |

## Logging

| Escolha | Justificativa |
|---|---|
| Logs JSON stdout | NFR-OBS-W01 |

## Testes

| Escolha | Justificativa |
|---|---|
| pytest | Unitários + integração leve |
| Hypothesis | P-VAL-01..07 (NFR-TEST-W02) |

## O que não usar neste ciclo (worker)

| Item | Motivo |
|---|---|
| FastAPI / Uvicorn | Sem HTTP (Q7=A) |
| pandas | Q3=A |
| Celery result backend | Q7=A |
| Prometheus | Q4=A |
| Import `lote_api` | Proibido (unit-of-work) |

## Dependências entre projetos

```text
lote-worker  -->  lote-shared  -->  SQLAlchemy/PyMySQL
lote-worker  -->  celery[redis]
lote-worker  -X->  lote-api   (proibido)
```

## Variáveis de ambiente (mínimo)

| Variável | Uso |
|---|---|
| `DATABASE_URL` | MySQL |
| `CELERY_BROKER_URL` | Valkey DB0 |
| `STORAGE_PATH` | Volume compartilhado (leitura) |
| `LOG_LEVEL` | Nível de log |
| `CELERY_CONCURRENCY` | Opcional; default 2 |

Valores concretos e serviço compose → Infrastructure Design.
