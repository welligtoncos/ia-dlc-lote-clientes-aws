# Plano — NFR Design: unit-infra-aws

**Base**: `nfr-requirements.md` (Q1–Q7=A, Q4 clarificado A) + functional-design

---

## Checklist (após respostas)

- [x] Gerar `nfr-design-patterns.md`
- [x] Gerar `logical-components.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Resiliência

A) Single-AZ conscientemente; backups RDS automatizados default AWS; sem Multi-AZ/failover custom neste ciclo

B) Read replica + failover script neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade

A) Desired count fixo = 1 para api e worker; capacity providers Fargate sem auto-scale policies

B) Target tracking CPU já neste design

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Desempenho

A) Sizing mínimo documentado em variables TF; sem reserved concurrency / performance modes especiais

B) Provisioned throughput / performance insights obrigatório neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança (padrões)

A) Defense-in-depth: privados + SG por tier; API Key só no Gateway; secrets injection ECS; SSE-S3; sem keys no state (sensitive + remote state)

B) WAF + Shield Advanced obrigatórios neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Componentes lógicos de plataforma

A) Módulos: `network`, `data` (rds+cache), `storage` (s3), `compute` (ecr+ecs+alb), `edge` (apigw+key), `security` (iam+secrets), `observability` (logs); root `envs/dev` compõe

B) Um módulo monolítico `lote_stack`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
