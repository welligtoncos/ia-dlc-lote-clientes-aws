# Perguntas — Design NFR unit-worker-validacao

Responda cada `[Answer]:` com a letra (ex.: `A`).

---

## Question 1 — Resiliência
Como materializar o **retry** da task `ingerir_clientes`?

A) `autoretry_for` / `retry_backoff` do Celery na própria task (3×, 60/120/240s) + `marcar_erro` só quando esgotar

B) Retry manual com `self.retry(...)` no código da task

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade / fila
Com `concurrency=2`, política de **ack/prefetch** preferida no MVP:

A) `task_acks_late=True` + `worker_prefetch_multiplier=1` (reentrega se o worker cair no meio)

B) Defaults do Celery (ack early; prefetch padrão)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Desempenho
Persistência do resultado no MySQL após validar o CSV:

A) **Uma** atualização ao final (`marcar_concluido` / `marcar_erro`) — contagens só em memória durante o parse (alinhado ao FD)

B) Flush periódico a cada N linhas (checkpoint parcial)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Segurança / config
Boot do worker (Settings):

A) Fail-fast: exige `DATABASE_URL`, `CELERY_BROKER_URL`, `STORAGE_PATH` (igual espírito da API)

B) Defaults embutidos para compose local (menos estrito)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Componentes lógicos
Conjunto mínimo de componentes lógicos do worker:

A) `CeleryApp` + `TaskIngerirClientes` + `LeitorCsv` + `ServicoValidacao` (usa lote-shared) + `LoteRepo` + `JsonLogger` + `Settings`

B) Apenas `CeleryApp` + task monolítica (tudo inline)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Cache da API
A API usa **cache-aside** Valkey em `GET /lotes/{id}`. Após o worker gravar `CONCLUIDO`/`ERRO`:

A) Worker **invalida** a chave `lote:{id}` (e lista se existir) no Valkey DB1 — evita leitura stale

B) Não invalidar; confiar no TTL curto da API

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Observabilidade
Correlação de logs no worker:

A) Usar `task_id` (+ `lote_id`) em todo log JSON da execução; campo `tentativa` = `request.retries + 1`

B) Somente `lote_id`

C) Outro (descreva após [Answer]:)

[Answer]: A
