# Plano — Infrastructure Design: unit-libs-storage

**Escopo**: fronteiras de infra da **lib** (env, volume local, contrato S3/IAM esperado).  
**Terraform completo** (bucket, roles, VPC) → `unit-infra-aws`.

---

## Checklist (após respostas)

- [x] Gerar `infrastructure-design.md`
- [x] Gerar `deployment-architecture.md`
- [x] Atualizar `shared-infrastructure.md` com contrato S3/env da lib (se aplicável)

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Ambiente de implantação (lib)

A) Lib **não** é implantável sozinha; roda dentro de imagens api/worker (ECS) e Compose

B) Publicar pacote privado (CodeArtifact) além do path install — neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 2 — Compute

A) N/A para a lib — compute = ECS Fargate / containers Compose dos consumidores

B) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Armazenamento

A) Documentar contrato: volume Compose (`diretorio_base`) + bucket S3 `lotes/` (criado por Terraform depois); lib só consome

B) Criar esqueleto Terraform do bucket **nesta** unit

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Mensageria

A) N/A nesta unit (fila = ElastiCache/Celery nos consumidores)

B) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Rede

A) N/A na lib; S3 via endpoint/gateway VPC fica em unit-infra-aws

B) Exigir VPC endpoint S3 já no contrato desta unit

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Monitoramento

A) Sem infra de monitoramento na lib; CloudWatch nos serviços ECS (consumidores)

B) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Infra compartilhada / env vars

A) Padronizar env: `STORAGE_BACKEND`, `STORAGE_LOCAL_DIR`, `S3_BUCKET`, `AWS_REGION`, `S3_PREFIX` (default `lotes/`)

B) Só `STORAGE_BACKEND` + `S3_BUCKET`; resto hardcoded defaults no código

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8 — IAM mínimo esperado (consumidores)

A) Documentar políticas lógicas: `s3:PutObject`, `GetObject`, `HeadObject` no prefixo `lotes/*` do bucket (implementação TF depois)

B) Não documentar IAM nesta unit

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 9 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
