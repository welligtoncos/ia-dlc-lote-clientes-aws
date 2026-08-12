# Intent Analysis — Serviço de Ingestão de Clientes

**Timestamp**: 2026-08-12T01:17:00Z
**Source**: `PRD-ingestao-clientes.md` (v1.0) + solicitação do usuário para gerar Inception

## Clareza da Solicitação
**Clara** — O PRD define visão, objetivos, RF/RNF, arquitetura hexagonal, modelo de dados, contrato de API, fluxo assíncrono, regras de validação, infra local/AWS e roadmap.

## Tipo de Solicitação
**Novo Projeto** (greenfield) — serviço de ingestão assíncrona de CSV de clientes.

## Estimativa Inicial de Escopo
**Múltiplos Componentes** — API FastAPI, worker Celery, Valkey (broker), MySQL (controle de lotes), Docker Compose; evolução AWS (ECS, ECR, ElastiCache, RDS, ALB, Secrets Manager, CloudWatch).

## Estimativa Inicial de Complexidade
**Moderada a Complexa** — fire-and-forget, hexagonal com PortaTarefa, allowlist de tasks, ciclo de status, validação de qualidade de dados, portabilidade local/AWS.

## Profundidade de Requisitos Escolhida
**Abrangente** — novo serviço com API pública, processamento assíncrono, persistência e NFRs explícitos; PRD completo, porém com questões em aberto (formato CSV, escopo MVP vs AWS, detalhes de retry/idempotência/armazenamento).

## Áreas a Esclarecer (pré-perguntas)
- Escopo desta entrega Inception/Construction (Fase 1 local vs incluir Fase 2 AWS)
- Formato CSV (cabeçalho, separador, encoding, tamanho máximo)
- Estratégia de armazenamento do arquivo entre upload e worker
- Política concreta de retry e idempotência
- Opt-in das extensões Security / Resiliency / PBT
