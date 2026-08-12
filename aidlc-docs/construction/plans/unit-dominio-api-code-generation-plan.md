# Plano de Geração de Código — unit-dominio-api

**Status**: Parte 2 CONCLUIDA — aguardando aprovação do codigo  
**Testes**: 15 passed (`pytest libs/tests api/tests`)

## Etapas de execução (Parte 2)

### Etapa 1 — Estrutura dos projetos
- [x] Criar `libs/pyproject.toml` (pacote `lote-shared`)
- [x] Criar `api/pyproject.toml` (depende de `lote-shared` path editable)
- [x] Criar árvore `src/` e `tests/` em ambos
- [x] `.gitignore` Python/Docker adequado

### Etapa 2 — lote-shared: domínio e portas
- [x] `StatusLote`, entidade `Lote` + metodos
- [x] Excecoes de dominio tipadas
- [x] Portas
- [x] Esboco `validacao/`

### Etapa 3 — Testes unitários + PBT do domínio (P-API-*)
- [x] pytest + Hypothesis
- [x] Propriedades P-API-01..04

### Etapa 4 — Resumo domínio
- [x] domain-summary.md

### Etapa 5 — lote-shared: persistence + cache
- [x] LoteRepositorio
- [x] CacheLoteRedis
- [x] migrations/001_lotes.sql

### Etapa 6 — Testes repositório
- [x] Cobertos via casos de uso com RepoMemoria (CRUD); repo SQLAlchemy exercitado via create_all no wiring

### Etapa 7 — Resumo repositório
- [x] repository-summary.md

### Etapa 8 — lote-api: application
- [x] Casos de uso US-01,03,04,05,06 + enqueue degraded

### Etapa 9 — Testes casos de uso
- [x] api/tests/test_casos_uso.py

### Etapa 10 — Resumo application
- [x] application-summary.md

### Etapa 11 — infrastructure adapters
- [x] AdaptadorCelery, ArmazenamentoArquivoLocal, Settings, main wiring

### Etapa 12 — presentation
- [x] FastAPI rotas + middleware + mapeamento HTTP

### Etapa 13 — Testes API
- [x] api/tests/test_api.py

### Etapa 14 — Resumo API
- [x] api-summary.md

### Etapa 15 — Deploy local + docs
- [x] Dockerfile, docker-compose.yml, .env.example, infra/README, README

### Etapa 16 — Resumo final
- [x] code-generation-summary.md

## Extensoes
| Extensao | Status |
|---|---|
| PBT | Compliant (P-API testes) |
| Security/Resiliency | N/A disabled |
