# Plano — Infrastructure Design: unit-api-cloud

**Escopo**: fronteiras env/imagem da **API** (Compose + contrato ECS).  
**Terraform Gateway/ALB/ECS** → `unit-infra-aws`.

---

## Checklist (após respostas)

- [x] Gerar `infrastructure-design.md`
- [x] Gerar `deployment-architecture.md`
- [x] Atualizar `shared-infrastructure.md` se necessário (env API)

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Ambiente de implantação

A) API continua como imagem Docker `api`; Compose local + alvo ECS Fargate (provisionado depois)

B) Mudar runtime (Lambda/EC2) neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Compute

A) Documentar: 1 task ECS api `dev` (CPU/mem a cargo do TF); Compose 1 container

B) Auto-scaling api já neste design

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Storage / mensageria (do ponto de vista da api)

A) API só **escreve** storage via lib + **enfileira** Celery; broker ElastiCache/Valkey via env

B) API lê S3 no request path

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Rede

A) API atrás de ALB privado; exposta via API Gateway (infra); Compose porta 8000

B) API com IP público direto

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Monitoramento

A) Logs stdout → CloudWatch (ECS); `/health` para ALB

B) APM (X-Ray/Datadog) obrigatório neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Env vars adicionais para dual enqueue

A) Confirmar uso: `STORAGE_BACKEND`, `S3_BUCKET`, `S3_PREFIX`, `AWS_REGION` (+ já existentes DB/broker/cache). Sem AWS keys na api

B) Exigir `AWS_ACCESS_KEY_ID` na api

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 7 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
