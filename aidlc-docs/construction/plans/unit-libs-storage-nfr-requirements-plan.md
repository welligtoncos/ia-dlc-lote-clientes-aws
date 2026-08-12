# Plano — NFR Requirements: unit-libs-storage

**Unidade**: biblioteca `lote-shared` (storage dual)  
**Base**: functional-design + `fase2-aws-requirements.md` + Security/Resiliency/PBT ON  
**Nota**: NFRs de plataforma (RDS Multi-AZ, API GW) ficam em `unit-infra-aws`; aqui só o que afeta a **lib de storage**.

---

## Checklist (após respostas)

- [x] Gerar `nfr-requirements.md`
- [x] Gerar `tech-stack-decisions.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Desempenho (salvar/abrir ≤ 5 MB)

A) Sem SLO rígido na lib; aceitável I/O síncrono bloqueante; foco em correção

B) Meta: `salvar`/`abrir` p95 < 2s em rede típica para objeto ≤ 5 MB (dev)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade da lib

A) Stateless; sem pool próprio; um client S3 por instância do adapter (suficiente para dev)

B) Client S3 compartilhado/singleton thread-safe obrigatório já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Disponibilidade / resiliência (nível lib)

A) Sem retry interno na lib (falhas sobem); retries ficam no Celery/worker ou SDK defaults mínimos

B) Retry com backoff na lib para erros transitórios S3 (ex.: 3 tentativas)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança (lib)

A) Sem credenciais no código; S3 via default credential chain; sem logs do conteúdo do CSV; refs ok em log

B) Além de A: sanitizar nomes de arquivo (rejeitar `..`, paths absolutos) na lib

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Stack cliente S3

A) `boto3` síncrono (alinha FastAPI sync + Celery prefork)

B) `aioboto3` / async (exigiria async na API)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Testes / manutenibilidade

A) Unitários Local + S3 com **moto** (ou equivalente) + PBT leve sobre invariantes da ref

B) Só unitários Local; S3 só em integração manual

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Dependência opcional boto3

A) `boto3` como dependência de `lote-shared` (sempre instalado)

B) Extra opcional `lote-shared[s3]`; Compose local sem boto3 se possível

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8 — Observabilidade

A) Sem métricas na lib; erros via exceções; logs ficam em api/worker

B) Logger estruturado opcional injetável na lib (debug put/get key, sem body)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 9 — Aprovar e gerar NFRs

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
