# Inventário de Componentes

## Pacotes de Aplicação
- `api/` (`lote-api`) — FastAPI + enqueue Celery
- `worker/` (`lote-worker`) — Celery worker + processamento CSV

## Pacotes Compartilhados
- `libs/` (`lote-shared`) — domínio, portas, persistence, cache, validação

## Pacotes de Infraestrutura
- `docker-compose.yml` — orquestração local
- `infra/` — esboço documental AWS (sem `.tf` ainda)
- `migrations/` — SQL init MySQL

## Pacotes de Teste
- `libs/tests` — PBT domínio/validação
- `api/tests` — casos de uso + TestClient
- `worker/tests` — leitor CSV + processador

## Contagem Total
- **Total de Pacotes Python**: 3
- **Aplicação**: 2 (api, worker)
- **Compartilhados**: 1 (libs)
- **Infraestrutura IaC**: 0 (pendente Terraform)
- **Teste**: embutidos nos 3 projetos
