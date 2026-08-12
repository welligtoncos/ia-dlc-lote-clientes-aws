# Plano de Unidades de Trabalho — Fase 2 Migração AWS

**Base**: `fase2-aws-execution-plan.md` · `fase2-aws-application-design.md` · `fase2-aws-stories.md`  
**As-is Fase 1**: `unit-dominio-api` + `unit-worker-validacao` + `libs`  
**Sequência sugerida no execution plan**: libs → api+worker → terraform → GHA/docs

---

## Checklist de geração (após aprovação deste plano + Q9)

- [x] Gerar `fase2-aws-unit-of-work.md`
- [x] Gerar `fase2-aws-unit-of-work-dependency.md`
- [x] Gerar `fase2-aws-unit-of-work-story-map.md`
- [x] Validar limites; todas as US-AWS-01..08 atribuídas
- [x] Não sobrescrever `unit-of-work*.md` da Fase 1

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Agrupamento de histórias / unidades

A) **4 unidades**: `unit-libs-storage` (S3+factory) · `unit-api-cloud` (wiring api/kwargs) · `unit-worker-s3` (task cloud) · `unit-infra-aws` (Terraform+GHA+docs dump/rollback/smoke)

B) **3 unidades**: `unit-app-cloud` (libs+api+worker juntos) · `unit-infra-terraform` · `unit-cicd-docs`

C) **5 unidades**: separar `unit-infra-terraform` e `unit-cicd-docs` da opção A

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Dependências / shared

A) Manter `lote-shared` como único pacote compartilhado; S3 entra em `libs/`; api e worker só sobem versão da lib

B) Extrair pacote novo `lote-aws` além de `lote-shared`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Ownership

A) Mesmo time/solo para todas as unidades Fase 2 (PRs por unidade)

B) Dono App (libs/api/worker) vs Dono Infra (Terraform/GHA/docs)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Considerações técnicas (deploy)

A) Unidades app = imagens ECR existentes evoluídas; unidade infra = Terraform state `dev` + workflow GHA (sem nova imagem)

B) Incluir imagem auxiliar (ex.: migrate/job) como unidade separada

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Domínio / bounded context

A) Contextos: **Storage Portability** (libs) · **Gestão de Lotes cloud** (api) · **Validação cloud** (worker) · **Platform AWS** (infra/CI)

B) Só dois contextos: **Application Cloud** vs **Platform AWS**

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Ordem Construction

A) libs-storage → api-cloud → worker-s3 → infra-aws (recomendado; alinhado ao execution plan)

B) infra-aws primeiro (para ter recursos), depois libs/api/worker

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Compose / dual backend

A) Regressão Compose `fs` coberta dentro das unidades app (AC em cada unit relevante)

B) Unidade extra só para “compat local”

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8 — US-AWS-07 (change mgmt) e US-AWS-08 (security)

A) Ambas na unidade de infra/CI (runbook, IAM, secrets, S3 privado)

B) Security espalhada: Key/Gateway na infra; secrets/IAM na infra; checks app nas units api/worker

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 9 — Aprovar plano

A) Aprovar — gerar artefatos de unidades conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
