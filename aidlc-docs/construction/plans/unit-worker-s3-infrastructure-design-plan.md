# Plano — Infrastructure Design: unit-worker-s3

**Escopo**: fronteiras env/imagem do **worker** (Compose + contrato ECS).  
**Terraform ECS/ElastiCache/Secrets** → `unit-infra-aws`.

---

## Checklist (após respostas)

- [x] Gerar `infrastructure-design.md`
- [x] Gerar `deployment-architecture.md`
- [x] Atualizar `shared-infrastructure.md` se necessário (env worker)

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Ambiente de implantação

A) Worker continua como imagem Docker `worker`; Compose local + alvo ECS Fargate (provisionado depois)

B) Mudar runtime (Lambda/EC2) neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Compute

A) Documentar: 1 task ECS worker `dev`; Compose 1 container com `--concurrency=2`

B) Autoscaling worker já neste design

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Storage / mensageria (ponto de vista do worker)

A) Worker **lê** storage via lib (`abrir`) + **consome** fila Celery; broker via env; MySQL via env

B) Worker escreve novos objetos S3 neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Rede

A) Worker só em rede privada (sem ALB/público); acesso S3/RDS/ElastiCache via VPC (infra)

B) Worker com IP público

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Monitoramento

A) Logs stdout → CloudWatch (ECS); sem APM obrigatório neste ciclo

B) APM (X-Ray/Datadog) obrigatório neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Env vars worker (dual + keys)

A) Confirmar: `STORAGE_BACKEND`, `STORAGE_LOCAL_DIR` (compose), `S3_BUCKET`, `S3_PREFIX`, `AWS_REGION`, e se s3: `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` (+ DB/broker existentes). Atualizar `.env.example`

B) Sem keys no worker (só task role IAM — contradiz FD/NFR Q4)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
