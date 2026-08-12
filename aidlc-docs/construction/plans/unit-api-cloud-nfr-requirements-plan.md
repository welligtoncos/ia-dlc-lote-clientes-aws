# Plano — NFR Requirements: unit-api-cloud

**Unidade**: `lote-api` — enqueue dual + HTTP  
**Base**: functional-design unit-api-cloud + NFRs Fase 1 api + Security/Resiliency ON  
**Fora**: Terraform/Gateway (unit-infra-aws); execução da task (unit-worker-s3)

---

## Checklist (após respostas)

- [x] Gerar `nfr-requirements.md`
- [x] Gerar `tech-stack-decisions.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Desempenho (POST 202)

A) Manter meta Fase 1: p95 POST `/lotes` < 300 ms local (enqueue sem processar CSV); tradução de kwargs no adapter com overhead negligível

B) Afrouxar SLO (só best-effort em `dev`)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade

A) Stateless; 1 réplica ECS suficiente em `dev`; sem sticky session

B) Exigir multi-réplica já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Disponibilidade / resiliência enqueue

A) Manter degrade: falha Celery → lote `PENDENTE` + log; sem retry de enqueue na API

B) Retry de enqueue na API (2–3x) antes de degradar

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança (API process)

A) Sem auth na app; secrets só via env; sem logar corpo CSV; confiar no SG/ALB privado + Gateway Key (infra)

B) Middleware API Key opcional (`REQUIRE_API_KEY=1`)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Stack (sem mudança de framework)

A) Manter FastAPI + Celery client + pydantic-settings; só evoluir AdaptadorCelery

B) Trocar cliente de fila neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Testes

A) Unitários do AdaptadorCelery (mock send_task) cobrindo fs vs s3 kwargs + regressão casos de uso

B) Só testes de casos de uso; adapter sem teste dedicado

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Observabilidade

A) Logs estruturados existentes; logar `lote_id` + backend no enqueue (sem body)

B) Métricas Prometheus já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8 — Aprovar e gerar NFRs

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
