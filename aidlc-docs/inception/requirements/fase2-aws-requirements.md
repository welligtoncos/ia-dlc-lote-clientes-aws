# Requisitos — Fase 2 Migração AWS

## Análise de Intenção

| Campo | Valor |
|---|---|
| Solicitação | Migrar MVP local de ingestão de clientes para AWS |
| Tipo | Migração + adaptação de código + deploy |
| Escopo | Sistema completo (infra Terraform + adapters + CI/CD) |
| Complexidade | Complexa |
| Profundidade | Abrangente |
| Base as-is | `aidlc-docs/inception/reverse-engineering/` |

### Decisões (Q1–Q13)

| # | Answer | Resumo |
|---|---|---|
| Q1 | A | Terraform + adapter S3 + ECS + API Gateway + smoke cloud |
| Q2 | A | Stack completo (RDS, APIGW, ALB, ECS, S3, ElastiCache, ECR) |
| Q3 | A | Região `us-east-1` |
| Q4 | A | Ambiente **dev** only (single-AZ, custo baixo) |
| Q5 | B | **API Key** no API Gateway |
| Q6 | A | Task kwargs `{lote_id, bucket, chave}`; nome `ingerir_clientes` |
| Q7 | A | Dual backend: filesystem no Compose; S3 se `STORAGE_BACKEND=s3` |
| Q8 | A | RDS `db.t4g.micro` (ou equiv.), single-AZ |
| Q9 | B | Incluir procedimento dump/restore MySQL local → RDS |
| Q10 | B | GitHub Actions: build/push ECR + **apply automático em dev** |
| Q11 | A | **Security Baseline ON** |
| Q12 | A | **Resiliency Baseline ON** |
| Q13 | A | **PBT completo ON** |

### Decisões Resiliency (CQ1–CQ4)

| # | Answer | Resumo |
|---|---|---|
| CQ1 | A | RTO/RPO **best-effort**; DR = **Backup & Restore** manual (snapshot RDS + versionamento S3) |
| CQ2 | A | Criticidade **Low** (dev/demo) |
| CQ3 | A | **Single-region** `us-east-1`, **single-AZ** |
| CQ4 | B | Change management **leve**: registro no PR/GHA + nota de rollback em README/runbook |

---

## 1. Visão do Produto (Fase 2)

Manter o comportamento funcional do MVP (upload CSV assíncrono, validação, consulta de lotes), implantado em AWS com:

- Entrada via **API Gateway** (API Key)
- Persistência em **RDS MySQL**
- Arquivos em **S3**
- Fila/cache em **ElastiCache**
- Compute **ECS Fargate** (api + worker)
- IaC **Terraform**
- CI/CD **GitHub Actions** com apply em `dev`

Compose local continua suportado com storage filesystem.

---

## 2. Requisitos Funcionais

| ID | Requisito | Origem |
|---|---|---|
| RF-AWS-01 | Provisionar stack `dev` em `us-east-1` via Terraform | Q1–Q4 |
| RF-AWS-02 | Expor API HTTP através de API Gateway → ALB → ECS `lote-api` | Q2, Q5 |
| RF-AWS-03 | Exigir **API Key** válida no API Gateway para rotas da API (exceto health se explicitamente liberado no design) | Q5 |
| RF-AWS-04 | Rodar worker Celery em serviço ECS separado (sem Gateway) | Q2 |
| RF-AWS-05 | Persistir lotes em **RDS MySQL**; aplicar schema `migrations/001_lotes.sql` | Q2, Q8 |
| RF-AWS-06 | Armazenar CSV em **S3** (prefixo `lotes/`) quando `STORAGE_BACKEND=s3` | Q2, Q6, Q7 |
| RF-AWS-07 | Evoluir enqueue/consumo: task `ingerir_clientes` com `{lote_id, bucket, chave}` | Q6 |
| RF-AWS-08 | Manter adapter filesystem para Compose (`STORAGE_BACKEND=fs` ou default local) | Q7 |
| RF-AWS-09 | Broker/cache via ElastiCache (DB0/DB1 equivalentes) | Q2 |
| RF-AWS-10 | Documentar e executar procedimento de **dump/restore** MySQL local → RDS (opcional na operação, obrigatório como artefato) | Q9 |
| RF-AWS-11 | Pipeline GitHub Actions: build imagens → push ECR → `terraform apply` no ambiente **dev** | Q10 |
| RF-AWS-12 | Smoke pós-deploy: health + POST `/lotes` + worker CONCLUIDO + GET via URL do Gateway | Q1 |
| RF-AWS-13 | Preservar RF do MVP: status PENDENTE→PROCESSANDO→CONCLUIDO/ERRO, reprocessar só ERRO, DELETE só DB | Fase 1 |
| RF-AWS-14 | Secrets (DB URL, broker, API keys de app se houver) via Secrets Manager / SSM — sem secrets no código | Security |
| RF-AWS-15 | IAM least-privilege: execution role + task roles api/worker (S3, secrets, logs, ECR) | Security |

---

## 3. Requisitos Não Funcionais

| ID | Categoria | Requisito | Origem |
|---|---|---|---|
| RNF-AWS-01 | Custo/dev | Single-AZ; RDS `db.t4g.micro` (ou equivalente) | Q4, Q8 |
| RNF-AWS-02 | Região | Primária `us-east-1` | Q3 |
| RNF-AWS-03 | Segurança | Security Baseline habilitado — controles bloqueantes nas fases de design/código | Q11 |
| RNF-AWS-04 | Segurança | API Key no Gateway; S3 privado; RDS sem IP público; SG restritivos | Q5, Q11 |
| RNF-AWS-05 | Segurança | Criptografia em trânsito (TLS no ALB/Gateway) e em repouso (RDS/S3 defaults) | Q11 |
| RNF-AWS-06 | Resiliência | Resiliency Baseline habilitado — orientação Well-Architected Reliability no design | Q12 |
| RNF-AWS-07 | Resiliência | Retry Celery existente mantido; health checks ECS/ALB; logs CloudWatch | Q12 + Fase 1 |
| RNF-AWS-13 | Resiliência | Criticidade **Low**; RTO/RPO best-effort; estratégia DR Backup & Restore manual | CQ1, CQ2 |
| RNF-AWS-14 | Resiliência | Topologia single-region / single-AZ em `us-east-1` (sem Multi-AZ neste ciclo) | CQ3 |
| RNF-AWS-15 | Resiliência | Proteção de dados: snapshots RDS manuais + versionamento S3; sem Pilot Light/Warm Standby | CQ1 |
| RNF-AWS-16 | Mudanças | Processo leve: PR + GitHub Actions como registro de mudança; nota de rollback em runbook/README | CQ4 |
| RNF-AWS-08 | Observabilidade | Logs JSON stdout → CloudWatch Logs (api e worker) | RNF-06 Fase 1 |
| RNF-AWS-09 | Portabilidade | Env vars (`DATABASE_URL`, `CELERY_BROKER_URL`, `CACHE_URL`, `STORAGE_BACKEND`, …) | Fase 1 |
| RNF-AWS-10 | Testes | PBT completo permanece; novos testes do adapter S3 / contrato kwargs | Q13 |
| RNF-AWS-11 | CI/CD | Apply automático só em **dev**; proteção de prod fora de escopo (não há prod neste ciclo) | Q10, Q4 |
| RNF-AWS-12 | Payload | API Gateway deve aceitar upload ≥ **5 MB** (RF-12 Fase 1) | Fase 1 |

---

## 4. Fora de escopo (este ciclo)

- Ambiente **prod** / Multi-AZ RDS
- Cognito/JWT (API Key apenas)
- LocalStack obrigatório
- Mudança de regras de validação de linha
- API Gateway na frente do worker

---

## 5. Critérios de aceite (Fase 2)

1. `terraform apply` (via CI ou equivalente) sobe stack **dev** sem erro.
2. Chamada autenticada com API Key: `POST /lotes` via URL do Gateway retorna 202.
3. Worker processa e `GET /lotes/{id}` retorna `CONCLUIDO` (ou `ERRO` legítimo).
4. Objeto CSV visível no bucket S3 sob `lotes/`.
5. Compose local ainda sobe e passa smoke com filesystem.
6. Procedimento dump/restore documentado e validado pelo menos uma vez (ou dry-run documentado).
7. Policies IAM / SGs revisadas sob Security Baseline.
8. Testes unitários + PBT relevantes verdes (incl. S3 fake/moto se aplicável).
9. Runbook/README com nota de rollback e PRs/GHA como trilha de mudança (CQ4=B).

---

## 6. Extensões

| Extensão | Enabled | Decided At |
|---|---|---|
| Security Baseline | **Yes** | Requirements Analysis Fase 2 (Q11=A) |
| Resiliency Baseline | **Yes** | Requirements Analysis Fase 2 (Q12=A); CQ1–CQ4 fechados |
| Property-Based Testing | **Yes** (full) | Requirements Analysis Fase 2 (Q13=A) |

### Conformidade Resiliency (Requirements)

| Regra | Status | Nota |
|---|---|---|
| RESILIENCY-01 | Conforme | Criticidade Low (CQ2=A) |
| RESILIENCY-02 | Conforme | Best-effort + Backup & Restore (CQ1=A) |
| RESILIENCY-03 | Conforme | Processo leve PR/GHA + rollback note (CQ4=B) |
| RESILIENCY-04 | Adiado | CI/CD/rollback/estilo — Design NFR / Construction |
| RESILIENCY-08 | Conforme | Single-region single-AZ (CQ3=A); multi-zone N/A (não é prod) |

Regras completas carregadas sob demanda nas fases Construction aplicáveis.
