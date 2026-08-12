# Unidades de Trabalho

**Projeto**: Serviço de Ingestão de Clientes (MVP local)  
**Decisões**: ver `plans/unit-of-work-plan.md`  
**Atualização**: projetos Python **segregados** (pedido do usuário) — cada unidade é um projeto instalável com `pyproject.toml` próprio.

---

## Visão geral

| Unidade | Projeto Python | Bounded context | Ownership | Imagem Docker |
|---|---|---|---|---|
| `unit-dominio-api` | `api/` (`lote-api`) | Gestão de Lotes | Dono API | Imagem `api` |
| `unit-worker-validacao` | `worker/` (`lote-worker`) | Validação de Qualidade | Dono Worker | Imagem `worker` |
| (compartilhado) | `libs/` (`lote-shared`) | Contratos + validação | Dono API | — (lib, não roda sozinha) |

**Regra**: `api` e `worker` **não** compartilham o mesmo `pyproject.toml` nem o mesmo venv de produção. Ambos dependem de `lote-shared` via path/editable install.

Ordem Construction: **1º unit-dominio-api (+ libs) → 2º unit-worker-validacao**.

---

## U1 — `unit-dominio-api` → projeto `lote-api`

### Responsabilidades
- Casos de uso e rotas FastAPI `/lotes`
- Adaptador Celery **somente enqueue** (cliente da fila)
- Armazenamento local do CSV + wiring HTTP
- Ownership de `lote-shared` (`libs/`)

### Não inclui
- Processo Celery worker / execução da task
- Dependências de runtime exclusivas do worker (ex.: pandas só no worker, se aplicável)

### Entregáveis
- Projeto Python `api/` com `pyproject.toml` (`lote-api`)
- `Dockerfile` da API
- Dependência: `lote-shared`
- Testes da API / casos de uso

### Histórias
US-01, US-03, US-04, US-05, US-06

---

## U2 — `unit-worker-validacao` → projeto `lote-worker`

### Responsabilidades
- Projeto Celery worker independente
- Task `ingerir_clientes`, retry, idempotência
- Lê CSV do volume; chama validadores de `lote-shared`; atualiza MySQL

### Não inclui
- Endpoints HTTP / FastAPI
- Alterações em `libs/` sem aprovação do dono da API

### Entregáveis
- Projeto Python `worker/` com `pyproject.toml` (`lote-worker`)
- `Dockerfile` do worker
- Dependência: `lote-shared`
- Testes da task + PBT (validadores em `lote-shared`)

### Histórias
US-02 (execução de US-01/US-05)

---

## Pacote compartilhado — `lote-shared` (`libs/`)

| Conteúdo | Motivo |
|---|---|
| `domain/` | `Lote`, portas |
| `validacao/` | Funções puras (PBT) |
| `persistence/` | Repositório MySQL (impl da porta) |

- `pyproject.toml` próprio (`lote-shared`)
- Versionado no monorepo; instalado com `pip install -e ../libs` (ou equivalente) em **api** e **worker**
- CODEOWNERS: dono da API

---

## Estratégia de organização de código (projetos Python separados)

```text
<repo>/   (monorepo — um git; TRÊS projetos Python)
├── libs/                         # Projeto 1: lote-shared
│   ├── pyproject.toml
│   ├── src/lote_shared/
│   │   ├── domain/
│   │   ├── validacao/
│   │   └── persistence/
│   └── tests/
├── api/                          # Projeto 2: lote-api  (unit-dominio-api)
│   ├── pyproject.toml            # deps: lote-shared, fastapi, uvicorn, ...
│   ├── src/lote_api/
│   │   ├── presentation/
│   │   ├── application/
│   │   └── infrastructure/       # AdaptadorCelery (enqueue), storage
│   ├── Dockerfile
│   └── tests/
├── worker/                       # Projeto 3: lote-worker  (unit-worker-validacao)
│   ├── pyproject.toml            # deps: lote-shared, celery, redis, ...
│   ├── src/lote_worker/
│   │   ├── celery_app.py
│   │   ├── tasks/
│   │   └── infrastructure/
│   ├── Dockerfile
│   └── tests/
├── docker-compose.yml            # sobe imagem api + imagem worker + valkey + mysql
└── aidlc-docs/
```

### Isolamento obrigatório
- [ ] Sem `pyproject.toml` único na raiz para runtime de api+worker
- [ ] Venvs / locks separados (`api` ≠ `worker`)
- [ ] Imports cruzados `lote_api` ↔ `lote_worker` **proibidos** — só via `lote_shared` + fila + volume + MySQL
- [ ] Dois Dockerfiles / duas imagens

**Desvio do PRD**: PRD sugeria pasta `app/` única e imagem única; este Inception define **projetos e imagens separados**.

---

## Extensões
| Extensão | Nota |
|---|---|
| PBT | Em `libs` (`lote_shared.validacao`), exercitado na Construction da U2 |
| Security / Resiliency | Desabilitados |
