# Perguntas — Requisitos Fase 2 (Migração AWS)

Responda cada `[Answer]:` com a letra (ex.: `A`).  
Decisões já sinalizadas aparecem como opção A quando aplicável — confirme ou altere.

---

## Question 1
Objetivo principal deste ciclo Fase 2?

A) Provisionar AWS (Terraform) + adaptar app (S3) + deploy ECS com API Gateway → smoke na cloud

B) Só Terraform (infra), sem mudar código da aplicação neste ciclo

C) Só adapter S3 + testes locais (LocalStack/MinIO), sem Terraform ainda

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2
Confirma o stack AWS?

A) Terraform + RDS MySQL + API Gateway (+ ALB → ECS) + S3 + ElastiCache + ECR/ECS Fargate (api e worker)

B) Igual A, mas sem ElastiCache (usar outro broker — descrever em X)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3
Região AWS padrão?

A) `us-east-1`

B) `sa-east-1` (São Paulo)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4
Ambientes a provisionar neste ciclo?

A) Apenas **dev** (single-AZ, custo baixo)

B) **dev** + esqueleto **prod** (prod sem apply obrigatório)

C) Só módulos reutilizáveis, sem workspace ambiente ainda

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5
Autenticação no API Gateway neste ciclo?

A) Nenhuma (igual MVP local) — só rede/throttling básico

B) API Key no Gateway

C) JWT / Cognito

D) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 6
Contrato da task Celery com S3?

A) Evoluir kwargs para `{lote_id, bucket, chave}` (ou `s3_uri`); manter nome `ingerir_clientes`

B) Manter `caminho` como string `s3://bucket/key` compatível

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7
Compatibilidade local após S3?

A) Manter adapter filesystem no Compose; S3 só quando `STORAGE_BACKEND=s3`

B) Tudo via S3 também no local (LocalStack/MinIO obrigatório)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8
RDS: classe / HA neste ciclo (dev)?

A) `db.t4g.micro` (ou equivalente barato), single-AZ, storage mínimo

B) `db.t4g.small`, single-AZ

C) Multi-AZ já neste ciclo

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 9
Escopo de dados na migração?

A) Ambiente cloud **novo/vazio** — só schema (`001_lotes.sql`); sem migrar dados do Compose

B) Incluir procedimento de dump/restore do MySQL local → RDS

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 10
CI/CD neste ciclo?

A) GitHub Actions: build/push ECR + `terraform plan` (apply manual)

B) GitHub Actions com apply automático em dev

C) Sem CI — Terraform/CLI local apenas

D) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 11 — Security Extensions
As regras da extensão de segurança devem ser aplicadas neste projeto?

A) Sim — aplicar todas as regras SECURITY como restrições bloqueantes (recomendado para produção)

B) Não — pular todas as regras SECURITY (PoC / experimental)

X) Other (please describe after [Answer]:)

[Answer]: A

---

## Question 12 — Resiliency Extensions
O baseline de resiliência deve ser aplicado neste projeto?

A) Sim — aplicar baseline de resiliência como orientação de design (Well-Architected Reliability)

B) Não — pular (PoC / iteração rápida)

X) Other (please describe after [Answer]:)

[Answer]: A

---

## Question 13 — Property-Based Testing Extension
As regras PBT devem continuar aplicadas?

A) Sim — todas as regras PBT (como na Fase 1)

B) Parcial — só funções puras / round-trips

C) Não — pular PBT neste ciclo

X) Other (please describe after [Answer]:)

[Answer]: A
