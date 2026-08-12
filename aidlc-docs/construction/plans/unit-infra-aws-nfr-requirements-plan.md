# Plano — NFR Requirements: unit-infra-aws

**Unidade**: Terraform + GHA + docs (`dev`)  
**Base**: functional-design (Q1–Q7=A)

---

## Checklist (após respostas)

- [x] Gerar `nfr-requirements.md`
- [x] Gerar `tech-stack-decisions.md`

**Nota Q4**: resposta `BB` corrigida para **A** via `unit-infra-aws-nfr-requirements-clarification.md`.

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Disponibilidade / resiliência

A) Best-effort `dev`: single-AZ; RTO/RPO best-effort (Inception); sem Multi-AZ / DR neste ciclo

B) Multi-AZ RDS + ElastiCache já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Desempenho / sizing

A) Tamanhos mínimos `dev` (ex.: RDS db.t4g.micro/small, cache cache.t4g.micro, Fargate 0.25–0.5 vCPU); sem SLO rígido de p95 na infra

B) Dimensionar para carga de produção já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Escalabilidade

A) 1 task ECS api + 1 task worker; sem autoscaling neste ciclo

B) Autoscaling ECS já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança (além do FD)

A) Confirmar: S3 encryption SSE-S3 (ou SSE-KMS default AWS); SG least-privilege; sem bastion público obrigatório (acesso via Session Manager opcional depois)

B) KMS CMK obrigatório + bastion EC2 neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A
<!-- corrigido de BB via clarification Q1=A -->

---

## Question 5 — Observabilidade

A) CloudWatch Logs (api/worker) + métricas ECS/ALB básicas; sem APM/X-Ray obrigatório

B) X-Ray + dashboards custom obrigatórios neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Stack IaC / CI

A) Terraform ≥ 1.5 + AWS provider; state remoto S3+DynamoDB (ou S3 lock); GHA OIDC (preferido) ou keys de CI em secrets do GitHub

B) State local apenas; apply só na máquina do desenvolvedor

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
