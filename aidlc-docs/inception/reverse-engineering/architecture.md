# Arquitetura do Sistema

**Estado atual**: MVP **local** (Docker Compose). Sem provisionamento AWS em código.

## Visão Geral

Monorepo com três projetos Python isolados (`lote-shared`, `lote-api`, `lote-worker`), orquestrados por um único `docker-compose.yml`. Comunicação assíncrona via Celery/Valkey; persistência MySQL; arquivos em volume compartilhado.

## Diagrama de Arquitetura (as-is)

```mermaid
flowchart TB
  Client[Cliente HTTP]
  subgraph compose [docker-compose]
    API[lote-api FastAPI :8000]
    W[lote-worker Celery]
    MySQL[(MySQL 8)]
    Valkey[(Valkey DB0 broker / DB1 cache)]
    Vol[(Volume lotes_files)]
  end
  Client --> API
  API --> MySQL
  API --> Vol
  API -->|send_task ingerir_clientes| Valkey
  Valkey --> W
  W --> MySQL
  W --> Vol
  W -->|invalidate| Valkey
  API -->|cache-aside GET| Valkey
```

## Diagrama de Interação — Ingestão

```mermaid
sequenceDiagram
  participant C as Cliente
  participant API as lote-api
  participant DB as MySQL
  participant FS as lotes_files
  participant Q as Valkey DB0
  participant W as lote-worker
  C->>API: POST /lotes
  API->>DB: Lote PENDENTE
  API->>FS: grava CSV
  API->>Q: ingerir_clientes{lote_id,caminho}
  API-->>C: 202
  Q->>W: entrega
  W->>FS: le CSV
  W->>DB: PROCESSANDO / CONCLUIDO ou ERRO
```

## Componentes

| Componente | Tipo | Papel |
|---|---|---|
| lote-api | Container / FastAPI | Borda HTTP |
| lote-worker | Container / Celery | Processamento |
| lote-shared | Biblioteca | Domínio + persistence + validação |
| MySQL | Dados | Tabela `lotes` |
| Valkey | Mensageria + cache | Broker + cache GET |
| Volume | Storage | CSV compartilhados |

## Lacunas vs alvo AWS (Fase 2 — decisões de produto)

| As-is | Alvo declarado |
|---|---|
| MySQL Compose | **RDS MySQL** |
| Porta 8000 | **API Gateway** → ALB → ECS API |
| Volume local | **S3** |
| Compose | **Terraform** + ECS Fargate |
| Valkey Compose | ElastiCache |

Nenhum `.tf` existe ainda; `infra/README.md` é esboço.
