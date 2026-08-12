# Plano — NFR Design: unit-api-cloud

**Base**: `nfr-requirements.md` (Q1–Q8=A) + functional-design (tradução no AdaptadorCelery)

---

## Checklist (após respostas)

- [x] Gerar `nfr-design-patterns.md`
- [x] Gerar `logical-components.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Resiliência (enqueue)

A) **Degrade pattern**: try/except no caso de uso (já existe); adapter propaga falhas do broker sem engolir

B) Circuit breaker no AdaptadorCelery

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade

A) Um `Celery` app client por processo api; sem pool custom

B) Singleton global de Celery no módulo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Desempenho

A) Tradução kwargs **síncrona em memória** (if/else backend); zero I/O

B) Consultar S3/head antes de enfileirar

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança

A) Adapter não recebe secrets S3; só `bucket` name + backend; credential chain fica no worker/task role

B) Passar access keys no payload da task

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Componentes lógicos

A) Evoluir só `AdaptadorCelery` (+ wiring em `main`/`settings`); casos de uso passam `ref` no payload

B) Novo serviço `TradutorTarefa` separado do adapter

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
