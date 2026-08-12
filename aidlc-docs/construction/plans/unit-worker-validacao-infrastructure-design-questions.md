# Perguntas — Design de Infraestrutura unit-worker-validacao

Responda cada `[Answer]:` com a letra (ex.: `A`).

---

## Question 1 — Ambiente de implantação
Como implantar o worker neste ciclo?

A) Serviço `worker` no **mesmo** `docker-compose.yml` da raiz (substituir placeholder); AWS só esboço (já em `infra/README.md`)

B) Compose separado só para worker

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Computação
Como rodar o processo Celery no container?

A) `celery -A lote_worker.celery_app worker --loglevel=INFO --concurrency=2` (imagem `worker/Dockerfile`)

B) concurrency via variável `CELERY_CONCURRENCY` (default 2) no comando do compose

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Armazenamento
Montagem do volume `lotes_files` no worker:

A) Mesmo path `/data/lotes` que a API (**read-write** no volume; worker só lê na prática)

B) Montagem **read-only** (`:ro`) em `/data/lotes`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Mensageria / cache
Conexões Valkey do worker:

A) `CELERY_BROKER_URL=redis://valkey:6379/0` + `CACHE_URL=redis://valkey:6379/1` (invalidação pós CONCLUIDO/ERRO)

B) Só broker DB0; invalidação de cache fora do MVP do worker

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Rede
Portas publicadas no host para o worker:

A) **Nenhuma** (só rede interna compose)

B) Expor porta de debug/flower

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Monitoramento
Observabilidade do worker no MVP local:

A) Apenas `docker compose logs worker` (JSON stdout); sem Flower/Prometheus

B) Incluir Flower neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Infra compartilhada
depends_on do serviço `worker`:

A) `mysql` (healthy) + `valkey` (started) — igual espírito da API

B) Só `valkey`

C) Outro (descreva após [Answer]:)

[Answer]: A
