# Plano — NFR Design: unit-worker-s3

**Base**: `nfr-requirements.md` (Q1–Q6=A) + functional-design (dual kwargs, `abrir`, keys se s3)

---

## Checklist (após respostas)

- [x] Gerar `nfr-design-patterns.md`
- [x] Gerar `logical-components.md`

**Nota Q4**: resposta inicial B corrigida para **A** via `unit-worker-s3-nfr-design-clarification.md` (Q1=A).

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Resiliência

A) Manter pattern Celery retry em `ErroRetentavel`; mapear falhas `abrir`/parse I/O → `ErroRetentavel`; sem circuit breaker

B) Circuit breaker em volta do S3 `abrir`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade

A) Um worker process Celery; concurrency via flag Compose (`--concurrency=2`); sem horizontal scale neste ciclo

B) Pool custom / prefetch tuning neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Desempenho

A) Abrir stream → parse CSV em memória (≤ 5 MB); sem prefetch/cache de objetos

B) Cache local de objetos S3 em disco

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança

A) Bootstrap: se backend s3, fail-fast sem ACCESS_KEY/SECRET; secrets só env; nunca no kwargs da task

B) Passar keys no payload Celery

C) Outro (descreva após [Answer]:)

[Answer]: A
<!-- corrigido de B via clarification Q1=A -->

---

## Question 5 — Componentes lógicos

A) Evoluir task + processador: resolver kwargs → `criar_armazenamento` → `abrir` → parse bytes; helper CSV de bytes se necessário

B) Novo módulo `ResolvedorArmazenamento` separado com DI formal

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
