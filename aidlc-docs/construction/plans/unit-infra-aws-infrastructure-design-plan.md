# Plano — Infrastructure Design: unit-infra-aws

**Escopo**: mapeamento concreto AWS `dev` (Terraform modules + GHA + runbooks).  
**Esta unit é a dona do provisionamento** (não só contrato).

---

## Checklist (após respostas)

- [x] Gerar `infrastructure-design.md`
- [x] Gerar `deployment-architecture.md`
- [x] Atualizar `shared-infrastructure.md` (contratos AWS)

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Ambiente / conta

A) Uma conta AWS `dev`; região `us-east-1`; naming `lote-*` / tag `Project=lote-clientes`, `Env=dev`

B) Contas separadas (dev/prod) já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Rede

A) VPC /16 com 1 AZ: 1 public subnet (ALB + NAT se necessário) + 2 private (app + data); SGs por tier

B) Só subnets públicas (simplificar) — não recomendado

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Data plane (RDS + cache + S3)

A) RDS MySQL 8 single-AZ; ElastiCache Redis/Valkey engine compatível single-node; S3 bucket privado `lotes/` SSE-S3

B) Aurora Serverless + MemoryDB neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Compute / edge

A) ECR (api+worker) → ECS Fargate desired=1; ALB interno/privado → API Gateway HTTP API (ou REST) + API Key; health `/health`

B) ECS em EC2 + NLB público sem Gateway

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — State + GHA

A) Backend TF: S3 state bucket + lock (DynamoDB ou S3 lock); workflow: on push main → build/push ECR → `terraform apply` `envs/dev`; credenciais via OIDC

B) State local + apply manual sem GHA

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Runbooks / docs paths

A) `infra/docs/`: `smoke-cloud.md`, `dump-restore-rds.md`, `rollback.md`; atualizar `infra/README.md`

B) Só README único sem runbooks separados

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
