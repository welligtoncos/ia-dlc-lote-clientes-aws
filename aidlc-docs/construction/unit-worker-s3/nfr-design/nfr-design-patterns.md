# Padrões NFR — unit-worker-s3

**Decisões**: Q1–Q3=A · Q4=A (corrigido via clarification) · Q5–Q6=A

---

## Resiliência — Celery retry (Q1=A)

| Padrão | Aplicação |
|---|---|
| Retry on `ErroRetentavel` | countdowns 60/120/240; max 3 |
| Map I/O → retentável | `ObjetoNaoEncontrado` / falhas `abrir` → `ErroRetentavel` |
| Sem circuit breaker | Em volta do S3 neste ciclo |

## Escalabilidade (Q2=A)

| Padrão | Aplicação |
|---|---|
| Concurrency Compose | `--concurrency=2` |
| Sem horizontal scale | 1 service ECS worker em `dev` (infra) |

## Desempenho (Q3=A)

| Padrão | Aplicação |
|---|---|
| Stream → parse | `abrir` → bytes/TextIO → CSV em memória (≤ 5 MB) |
| Sem cache local | Sem prefetch/disco de objetos S3 |

## Segurança (Q4=A — clarification)

| Padrão | Aplicação |
|---|---|
| Fail-fast bootstrap | Se `STORAGE_BACKEND=s3` e faltam ACCESS_KEY/SECRET → erro na subida |
| Secrets só env/Secrets Manager | Nunca em kwargs Celery / payload |
| Payload limpo | Só `lote_id` + `caminho` **ou** `bucket`+`chave` |

## Mapeamento NFR → padrão

| NFR | Padrão |
|---|---|
| NFR-WRK-AVAIL-* | Celery retry + map I/O |
| NFR-WRK-SCALE-* | concurrency=2; 1 réplica |
| NFR-WRK-PERF-* | stream → parse ≤ 5 MB |
| NFR-WRK-SEC-* | fail-fast keys env; sem secrets no broker |
