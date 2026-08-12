# Padrões de Design NFR — unit-worker-validacao

**Decisões**: Q1–Q7 = A

---

## Resiliência — Celery autoretry

**Padrão**: *Autoretry com backoff + falha terminal no domínio*

1. Task `ingerir_clientes` configura `autoretry_for` (exceções transitórias: I/O, DB, cabeçalho inválido tratado como falha retentável conforme FD).
2. `max_retries=3`, backoff alinhado a **60s / 120s / 240s** (`retry_backoff` / countdown equivalente).
3. Enquanto houver retry: **não** chamar `marcar_erro` (lote pode permanecer `PENDENTE` se header falhou antes de `PROCESSANDO`).
4. Após esgotar retries: `marcar_erro(mensagem)` + persistir + invalidar cache.
5. Idempotência: guard no início (`CONCLUIDO` + mesmo `task_id` → NOOP sem retry).

## Escalabilidade — ack late + prefetch 1

**Padrão**: *At-least-once delivery-friendly*

- `task_acks_late=True`
- `worker_prefetch_multiplier=1`
- `concurrency=2` (NFR Requirements)
- Se o processo cair no meio, a mensagem pode ser reentregue; guard de idempotência + retry-do-zero protegem o estado final.

## Desempenho — parse streaming + write-once

**Padrão**: *Single final write*

- `LeitorCsv` (stdlib `csv`) stream linha a linha.
- Contagens só em memória.
- **Uma** persistência MySQL ao final: `marcar_concluido` ou `marcar_erro`.
- Sem checkpoint parcial.

## Segurança — configuração

**Padrão**: *12-factor config + fail-fast startup*

- `Settings` exige `DATABASE_URL`, `CELERY_BROKER_URL`, `STORAGE_PATH`.
- Sem secrets no código; `.env.example` na raiz do monorepo.
- Sem porta HTTP exposta.

## Cache consistency (cross-unit)

**Padrão**: *Write-through invalidation from consumer*

- Após persistir `CONCLUIDO` ou `ERRO`, invalidar Valkey DB1:
  - `lote:{id}`
  - chave de lista (ex.: `lotes:lista`) se a API a usar
- Evita GET stale na API após o worker terminar.
- Falha na invalidação: log warning (não reverte o status MySQL — fonte da verdade é o banco).

## Observabilidade

**Padrão**: *Task correlation*

- Todo log JSON inclui `task_id`, `lote_id`, `tentativa` (`request.retries + 1`), `duracao_ms`, `status_final`.
- Eventos-chave: start, header_ok/header_fail, noop_idempotent, concluido, erro_terminal.

## Mapa NFR → padrão

| NFR | Padrão |
|---|---|
| NFR-REL-W01/W02 | Celery autoretry + retry-do-zero |
| NFR-REL-W03 | Guard idempotente |
| NFR-SCALE-W01 | concurrency=2 + acks_late + prefetch=1 |
| NFR-PERF-W02 | Streaming csv + write-once |
| NFR-SEC-W01 | Settings fail-fast |
| NFR-OBS-W01/W02 | JSON + task_id correlation |
| Cache API | Invalidação Valkey DB1 pós-write |
