# Padrões de Design NFR — unit-dominio-api

**Decisões**: Q1=A · Q2=C (confirmado CQ1=A) · Q3=A · Q4=B · Q5=A · Q6=A

---

## Resiliência — enqueue tolerante

**Padrão**: *Degraded enqueue* (try/except no AdaptadorCelery)

1. Persistir `Lote` + arquivo no volume.
2. Tentar `PortaTarefa.executar(...)`.
3. Se broker falhar: log `error` com `lote_id` + exceção; `celery_task_id` permanece nulo; resposta HTTP **202** mantida.
4. Recuperação: `PUT /lotes/{id}` (reprocessar) quando broker voltar.

Não usa outbox nem circuit breaker fail-fast neste MVP.

## Escalabilidade — leituras

**Padrão**: *Cache-aside* em Valkey para `GET /lotes/{id}` (e opcionalmente lista)

- Chave sugerida: `lote:{id}` → JSON serializado do lote.
- TTL curto (ex.: 30–60 s) — valor exato no Infrastructure Design.
- Invalidação: após mutações (POST sucesso, PUT reprocessar, DELETE) → `DEL lote:{id}` (+ invalidar lista se cacheada).
- Valkey já existe como broker; **mesmo cluster/instância** pode servir DB lógico separado (ex.: Redis db=1) ou prefixo `cache:` — detalhe no Infrastructure Design.
- Carga MVP baixa: overhead aceito explicitamente (CQ1=A) para exercitar o padrão.

Escrita/POST: **sem** cache; sempre MySQL + volume.

## Desempenho — POST

**Padrão**: *Fast path sem parse*

- Gravar stream do upload direto no volume.
- Insert MySQL do lote.
- Enqueue (best-effort).
- **Não** ler/parsear CSV na API.
- Timeout HTTP do Uvicorn dimensionado para upload ≤ 5 MB (infra).

## Segurança — configuração

**Padrão**: *12-factor config + fail-fast startup*

- Pydantic Settings: apenas env.
- Sem senhas default no código; `.env.example` com placeholders.
- Startup valida presença de `DATABASE_URL` e `CELERY_BROKER_URL` (e `STORAGE_PATH`); aborta se ausentes.

## Observabilidade

**Padrão**: *Request correlation*

- Middleware gera UUID `request_id`.
- Inclui em todos os logs JSON da request.
- Echo no header de resposta `X-Request-ID`.
- Campos: request_id, lote_id (quando houver), método, path, status, latência_ms.

## Mapa NFR → padrão

| NFR | Padrão |
|---|---|
| NFR-REL-01/02 | Degraded enqueue |
| NFR-SCALE-02 + Q2 | Cache-aside Valkey (GET) |
| NFR-PERF-01 | Fast path upload |
| NFR-SEC-01 | Settings + fail-fast env |
| NFR-OBS-01/02 | JSON logs + request_id |
| NFR-AVAIL-01 | Best-effort + `GET /health` leve |
