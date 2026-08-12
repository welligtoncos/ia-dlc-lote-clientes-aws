# Requisitos NFR — unit-worker-s3

**Decisões**: Q1–Q6 = A

---

## Desempenho

| ID | Requisito |
|---|---|
| NFR-WRK-PERF-01 | Best-effort; processamento síncrono do CSV ≤ **5 MB**; sem SLO rígido de p95 neste ciclo |
| NFR-WRK-PERF-02 | Leitura via streaming/`abrir` da lib; sem carregar objeto S3 além do necessário para o parse |

## Escalabilidade

| ID | Requisito |
|---|---|
| NFR-WRK-SCALE-01 | Celery **concurrency=2** no Compose (padrão existente) |
| NFR-WRK-SCALE-02 | Em `dev` AWS: **1** service ECS worker; **sem** autoscaling neste ciclo |

## Disponibilidade / resiliência

| ID | Requisito |
|---|---|
| NFR-WRK-AVAIL-01 | Manter retry Celery **3×** com countdowns **60 / 120 / 240** s |
| NFR-WRK-AVAIL-02 | Falhas de arquivo/S3 (`ObjetoNaoEncontrado`, I/O) → `ErroRetentavel` |
| NFR-WRK-AVAIL-03 | Idempotência `CONCLUIDO` + mesmo `task_id` → NOOP (Fase 1) |

## Segurança

| ID | Requisito |
|---|---|
| NFR-WRK-SEC-01 | Se `STORAGE_BACKEND=s3` (ou task em modo s3): exigir `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |
| NFR-WRK-SEC-02 | Credenciais só via env / Secrets Manager (runtime); nunca no código |
| NFR-WRK-SEC-03 | Não logar conteúdo do CSV; ok `lote_id`, backend, chave/caminho sanitizado |

## Observabilidade

| ID | Requisito |
|---|---|
| NFR-WRK-OBS-01 | Logs estruturados existentes; indicar modo `fs`/`s3` no início do processamento |
| NFR-WRK-OBS-02 | Sem Prometheus / métricas custom neste ciclo |

## Testes / manutenibilidade

| ID | Requisito |
|---|---|
| NFR-WRK-TEST-01 | Testes do processador/task com storage memória ou moto; kwargs **fs** e **s3** |
| NFR-WRK-TEST-02 | Regressão fluxo local Compose (`STORAGE_BACKEND=fs`) |

## Usabilidade (operacional)

| ID | Requisito |
|---|---|
| NFR-WRK-OPS-01 | Dual kwargs transparentes ao operador; mesma task name `ingerir_clientes` |

## Extensões

| Extensão | Nota |
|---|---|
| Security | SEC-* keys + sem log CSV |
| Resiliency | AVAIL retry/idempotência; RTO/RPO best-effort global |
| PBT | N/A novo (validação já em `lote_shared`) |
