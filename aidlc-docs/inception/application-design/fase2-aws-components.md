# Componentes — Fase 2 Migração AWS

**Decisões**: Q1=A · Q2=A · Q3=A · Q4=A · Q5=A · Q6=A  
**Base**: hexagonal C1–C4 Fase 1; este doc descreve **deltas** e componentes tocados.

---

## C1 — Domain *(sem mudança estrutural)*

| Campo | Descrição |
|---|---|
| **Propósito** | Núcleo do negócio |
| **Delta Fase 2** | Nenhum. `PortaArmazenamentoArquivo` mantém `salvar` → `str` (referência opaca) e `existe` |
| **Não faz** | Conhecer S3, bucket ou API Gateway |

---

## C2 — Application *(delta mínimo)*

| Campo | Descrição |
|---|---|
| **Propósito** | Casos de uso e validação pura |
| **Delta Fase 2** | Continua recebendo `ref` opaca do storage; **não** monta `bucket`/`chave`. Payload da task: `{lote_id, ref}` ou dict mínimo; tradução cloud fica na Infrastructure (Q3=A) |
| **Não faz** | Escolher backend `fs`/`s3`; validar API Key |

---

## C3 — Infrastructure *(delta principal app)*

| Campo | Descrição |
|---|---|
| **Propósito** | Adaptadores concretos |
| **Delta Fase 2** | `ArmazenamentoArquivoS3` em `libs`; factory `criar_armazenamento(STORAGE_BACKEND)`; `AdaptadorCelery` traduz `ref` → kwargs `{lote_id, bucket, chave}` ou `{lote_id, caminho}`; task worker lê S3 quando kwargs cloud |
| **Não faz** | Regras de validação de linha |

### Subcomponentes novos / evoluídos
| ID | Nome | Pacote |
|---|---|---|
| C3a | ArmazenamentoArquivoLocal | libs (existente) |
| C3b | ArmazenamentoArquivoS3 | libs (**novo**) |
| C3c | FactoryStorage | libs composition helper (**novo**) |
| C3d | AdaptadorCelery + task | api/worker (evoluir kwargs) |
| C3e | LoteRepositorio | inalterado (RDS via URL) |

---

## C4 — Presentation *(delta mínimo)*

| Campo | Descrição |
|---|---|
| **Propósito** | HTTP FastAPI |
| **Delta Fase 2** | Sem validação de API Key (Q4=A — só Gateway). Composition root escolhe storage via env |
| **Não faz** | Terraform / GHA |

---

## C5 — Composition Root *(explícito Fase 2)*

| Campo | Descrição |
|---|---|
| **Propósito** | Wire adapters conforme env |
| **Responsabilidades** | Ler `STORAGE_BACKEND`, `S3_BUCKET`, `AWS_REGION`, `DATABASE_URL`, broker; instanciar factory storage; injetar nos casos de uso / worker |
| **Onde** | `api` main + bootstrap `worker` |
| **Histórias** | US-AWS-02, US-AWS-04 |

---

## Fora do Application Design (Q5=A)

| Fronteira | Documento futuro |
|---|---|
| Terraform stack, API Gateway API Key, IAM roles, GHA | Infrastructure Design / Units |
| App **assume**: task role com S3; secrets via env injetado do SM/SSM; rede privada ALB→ECS |

---

## Mapa Componente → Histórias Fase 2

| Componente | US-AWS |
|---|---|
| C3b/C3c/C5 | 02, 04 |
| C3d worker | 03 |
| C4 + Gateway (fronteira) | 01 |
| C3e RDS URL | 05, 06 |
| Security/IAM (fronteira) | 08 |
