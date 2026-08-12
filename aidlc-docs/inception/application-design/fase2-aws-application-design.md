# Design da Aplicação — Fase 2 Migração AWS (consolidado)

## Decisões do plano

| Q | Answer | Resumo |
|---|---|---|
| Q1 | A | S3 + factory em `libs`; api/worker consomem porta |
| Q2 | A | `PortaArmazenamentoArquivo` estável; ref opaca |
| Q3 | A | Application passa `ref`; Infra traduz kwargs fs vs s3 |
| Q4 | A | API Key só no API Gateway |
| Q5 | A | Terraform/GHA fora deste estágio (fronteiras apenas) |
| Q6 | A | Factory no composition root |
| Q7 | A | Plano aprovado |

## Artefatos

| Doc | Conteúdo |
|---|---|
| [fase2-aws-components.md](./fase2-aws-components.md) | C1–C5 deltas |
| [fase2-aws-component-methods.md](./fase2-aws-component-methods.md) | Assinaturas |
| [fase2-aws-services.md](./fase2-aws-services.md) | Orquestração cloud vs local |
| [fase2-aws-component-dependency.md](./fase2-aws-component-dependency.md) | Matriz e fluxos |

## Visão resumida

Hexagonal Fase 1 preservado. Delta de aplicação: **adapter S3 + factory + tradução de kwargs Celery + composition root por env**. Auth e provisionamento ficam no edge/infra.

## Próximo estágio

**Geração de Unidades** — decompor libs / api / worker / terraform / CI conforme `fase2-aws-execution-plan.md`.

## Conformidade extensões (Application Design)

| Extensão | Status | Nota |
|---|---|---|
| Security Baseline | Parcial / fronteira | Key no Gateway; secrets/IAM no Infra Design |
| Resiliency Baseline | N/A neste artefato | Topologia já nos requisitos |
| PBT | Conforme | Validadores puros inalterados; novos testes no adapter S3 na Construction |
