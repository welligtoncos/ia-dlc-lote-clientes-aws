# Plano — Design Funcional: unit-infra-aws

**Unidade**: `unit-infra-aws` (`infra/terraform` + GHA + docs)  
**Histórias**: US-AWS-01 · US-AWS-05 · US-AWS-06 · US-AWS-07 · US-AWS-08  
**Depende de**: contratos env api/worker/libs já aprovados  

**Nota**: “Design funcional” aqui = políticas operacionais e regras de plataforma (não domínio de clientes/lotes).

---

## Checklist (após respostas)

- [x] Gerar `business-logic-model.md`
- [x] Gerar `business-rules.md`
- [x] Gerar `domain-entities.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Escopo Terraform `dev` (US-AWS-05)

A) Stack completa single-AZ `us-east-1`: VPC/SG, RDS MySQL, S3, ElastiCache (Valkey/Redis), ECR, ECS api+worker, ALB, API Gateway HTTP/REST + API Key, IAM, Secrets, CloudWatch Logs

B) Só rede + RDS + S3 neste ciclo (ECS/Gateway depois)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Layout do código Terraform

A) `infra/terraform/` com módulos (`vpc`, `rds`, `s3`, `elasticache`, `ecs`, `gateway`, …) + root `dev`

B) Um único `main.tf` monolítico sem módulos

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — API Key (US-AWS-01)

A) API Key **criada/gerenciada no Terraform**; valor sensível em output sensível / Secrets Manager; cliente usa header `x-api-key`

B) API Key só criada manualmente no console; TF só referencia usage plan

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Secrets / credenciais app (ACCESS_KEY, DB)

A) Secrets Manager (ou SSM SecureString) injetados como env nas task defs ECS; TF cria secrets placeholders; valores sensíveis fora do git

B) Variáveis plain no `terraform.tfvars` commitável

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Dump/restore e rollback (US-AWS-06 / US-AWS-07)

A) Runbooks markdown: dump/restore RDS (mysqldump), nota de rollback (TF previous apply / redeploy tag ECR), smoke checklist pós-deploy

B) Automação completa de dump no GHA neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Change management / Security (US-AWS-07 / US-AWS-08)

A) PR obrigatório para mudanças TF/GHA; apply automático só em `dev` via GHA após merge; S3 privado + block public; RDS/ElastiCache privados; least-privilege IAM; TLS no edge Gateway

B) Apply local sem PR neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
