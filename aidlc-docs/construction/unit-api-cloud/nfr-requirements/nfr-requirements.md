# Requisitos NFR — unit-api-cloud

**Decisões**: Q1–Q8 = A

---

## Desempenho

| ID | Requisito |
|---|---|
| NFR-API-PERF-01 | POST `/lotes` p95 **< 300 ms** (compose local, ≤ 5 MB), sem processar CSV |
| NFR-API-PERF-02 | Tradução de kwargs no AdaptadorCelery com overhead negligível (sem I/O extra) |

## Escalabilidade

| ID | Requisito |
|---|---|
| NFR-API-SCALE-01 | Processo **stateless**; 1 réplica ECS suficiente em `dev` |
| NFR-API-SCALE-02 | Sem sticky session / estado em memória além de clients |

## Disponibilidade / resiliência

| ID | Requisito |
|---|---|
| NFR-API-AVAIL-01 | Falha no enqueue Celery → lote permanece `PENDENTE` + log (degrade Fase 1) |
| NFR-API-AVAIL-02 | **Sem** retry de enqueue na API |

## Segurança

| ID | Requisito |
|---|---|
| NFR-API-SEC-01 | Sem autenticação na FastAPI; API Key no Gateway (infra) |
| NFR-API-SEC-02 | Secrets/URLs só via env |
| NFR-API-SEC-03 | Não logar corpo do CSV; ok logar `lote_id` + backend |

## Observabilidade

| ID | Requisito |
|---|---|
| NFR-API-OBS-01 | Logs estruturados existentes; enriquecer enqueue com backend (`fs`/`s3`) |
| NFR-API-OBS-02 | Sem Prometheus neste ciclo |

## Testes / manutenibilidade

| ID | Requisito |
|---|---|
| NFR-API-TEST-01 | Unitários AdaptadorCelery (mock `send_task`) — kwargs fs vs s3 |
| NFR-API-TEST-02 | Regressão casos de uso / API existentes |

## Usabilidade

| ID | Requisito |
|---|---|
| NFR-API-UX-01 | Contrato HTTP OpenAPI inalterado para clientes |

## Extensões

| Extensão | Nota |
|---|---|
| Security | SEC-* na app; edge Key → infra |
| Resiliency | AVAIL degrade; RESILIENCY-04 deploy → infra/NFR global |
| PBT | N/A novo nesta unit (validação já na lib) |
