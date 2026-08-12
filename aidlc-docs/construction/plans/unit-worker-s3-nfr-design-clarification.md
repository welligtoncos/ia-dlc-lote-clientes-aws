# Esclarecimento — NFR Design unit-worker-s3 (Q4)

**Conflito detectado**: no plano NFR Design, **Q4 = B** (“Passar keys no payload Celery”).

Isso **contradiz** decisões já aprovadas:

| Artefato | Decisão |
|---|---|
| Functional Design `RN-SEC01` | Keys via env no worker se s3 |
| NFR Requirements `NFR-WRK-SEC-01/02` | Keys via env/Secrets; nunca no código |
| unit-api-cloud NFR Design Q4=A | Adapter **não** coloca secrets no payload |

**Risco**: keys em kwargs Celery ficam no broker (Valkey/ElastiCache), logs e retries.

---

## Question 1 — Confirmar política de credenciais S3 no worker

A) **Corrigir Q4 para A**: bootstrap fail-fast; keys **só** via env/Secrets; **nunca** no payload da task (alinhado ao aprovado)

B) **Manter Q4=B**: passar `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` nos kwargs Celery (sobrescreve NFR/FD de segurança — não recomendado)

C) Outro (descreva após [Answer]:)

[Answer]: A
