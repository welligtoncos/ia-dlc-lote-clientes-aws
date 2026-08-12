# Plano — NFR Requirements: unit-worker-s3

**Unidade**: `lote-worker` — consumo dual fs/s3  
**Base**: functional-design (Q1–Q3=A, Q4=B, Q5=A)

---

## Checklist (após respostas)

- [x] Gerar `nfr-requirements.md`
- [x] Gerar `tech-stack-decisions.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Desempenho

A) Best-effort; processamento síncrono do CSV ≤ 5 MB; sem SLO rígido além do retry existente

B) Meta p95 < 30s por lote em `dev`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade

A) concurrency Celery=2 (Compose); 1 service ECS worker `dev` sem autoscaling neste ciclo

B) Autoscaling worker já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Resiliência

A) Manter retry Celery 3× 60/120/240; falhas S3/arquivo → ErroRetentavel

B) Mudar política de retry

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança

A) Keys obrigatórias se s3 (Q4=B FD); sem logar CSV; credential via env/Secrets

B) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Stack / testes

A) Manter Celery + lote-shared; testes processador com storage memória/moto; dual kwargs

B) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
