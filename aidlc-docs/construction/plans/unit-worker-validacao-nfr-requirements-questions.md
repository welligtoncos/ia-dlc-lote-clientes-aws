# Perguntas — Requisitos NFR unit-worker-validacao

Responda cada `[Answer]:` com a letra (ex.: `A`).

---

## Question 1
Meta de **desempenho** para processar um CSV de até **5 MB** (~ordem de dezenas de milhares de linhas) no MVP local (1 worker):

A) Best-effort — sem SLO formal; concluir em minutos é aceitável

B) Meta soft: concluir em **< 60 s** na máquina de desenvolvimento típica

C) Meta soft: concluir em **< 10 s**

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2
**Concorrência** do worker Celery no compose MVP:

A) **1** worker process, **concurrency=1** (processa um lote por vez)

B) 1 worker process, concurrency=2

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 3
Biblioteca para **ler/parsear CSV** no worker:

A) Módulo padrão `csv` (stdlib) — streaming linha a linha

B) `pandas.read_csv`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4
**Observabilidade** do worker (alinhada à API):

A) Logs JSON em stdout com `lote_id`, `task_id`, tentativa, duração, status final

B) Logs texto simples (não JSON)

C) JSON + métricas Prometheus neste ciclo

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5
**Limites de tempo** da task Celery (`ingerir_clientes`):

A) Sem soft/hard time limit explícito no MVP (confiar no retry + máquina local)

B) Soft limit 5 min / hard limit 6 min

C) Soft limit 2 min / hard limit 3 min

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6
Se o arquivo CSV for **maior que o esperado em linhas** mas ainda ≤ 5 MB (upload já passou na API):

A) Processar normalmente sem limite extra de linhas

B) Abortar com `ERRO` se `total_linhas` (não-branco) exceder um teto (ex.: 100_000)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7
Stack Python do projeto `lote-worker` (além de `lote-shared`):

A) Celery + redis/Valkey broker + SQLAlchemy via shared + pytest/Hypothesis — **sem FastAPI**

B) Mesmo que A, mas com result backend Redis habilitado

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8
Escopo de **testes** NFR/qualidade nesta unidade:

A) Unitários da task + PBT P-VAL-01..07 em `lote-shared` + teste de integração leve (task com repo/arquivo fake)

B) Somente unitários + PBT (sem teste de integração da task)

C) Outro (descreva após [Answer]:)

[Answer]: A
