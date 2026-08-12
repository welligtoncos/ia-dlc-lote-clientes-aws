# Requisitos NFR — unit-dominio-api

**Unidade**: unit-dominio-api (`lote-api` + ownership `lote-shared`)  
**Decisões do plano**: Q1=A, Q2=A, Q3=A, Q4=A, Q5=A, Q6=A, **Q7=B**, Q8=A

---

## Desempenho

| ID | Requisito |
|---|---|
| NFR-PERF-01 | `POST /lotes` responde **202** com p95 **< 300 ms** para arquivos ≤ 5 MB (compose local), sem processar o CSV |
| NFR-PERF-02 | Leituras `GET /lotes` e `GET /lotes/{id}` p95 < 200 ms com volume de dados de MVP (< milhares de lotes) |

## Escalabilidade

| ID | Requisito |
|---|---|
| NFR-SCALE-01 | Carga MVP: **< 10 req/min**; **1** instância `api` suficiente |
| NFR-SCALE-02 | Código sem estado de sessão; escala horizontal futura por réplicas (não exigida neste ciclo) |

## Disponibilidade

| ID | Requisito |
|---|---|
| NFR-AVAIL-01 | Best-effort (dev/demo): **sem SLA** |
| NFR-AVAIL-02 | Recuperação: restart manual do `docker-compose` |

## Segurança (MVP)

| ID | Requisito |
|---|---|
| NFR-SEC-01 | Credenciais e URLs sensíveis **somente** via variáveis de ambiente |
| NFR-SEC-02 | Sem autenticação/autorização neste ciclo |
| NFR-SEC-03 | Sem TLS obrigatório no ambiente local |
| NFR-SEC-04 | Limite de upload 5 MB permanece como regra de negócio (RN-U03), não como controladora extra além do já definido |

## Observabilidade

| ID | Requisito |
|---|---|
| NFR-OBS-01 | Logs **estruturados JSON** em stdout |
| NFR-OBS-02 | Campos mínimos: `request_id`, `lote_id` (quando houver), latência, método, path, status HTTP |
| NFR-OBS-03 | Sem métricas Prometheus neste ciclo |

## Confiabilidade / enqueue

| ID | Requisito |
|---|---|
| NFR-REL-01 | Se o **broker estiver indisponível** no `POST /lotes`: **ainda assim** criar lote `PENDENTE`, persistir arquivo e retornar **202** (quando possível após persistência) |
| NFR-REL-02 | Falha de enqueue **não** reverte o lote; recuperação via `PUT` reprocessar (US-05) ou operação operacional |
| NFR-REL-03 | Logar erro de enqueue com `lote_id` e motivo (nível error) |
| NFR-REL-04 | Status canônico do lote permanece no MySQL |

> **Implicação**: podem existir lotes `PENDENTE` sem `celery_task_id` até reprocessamento/enqueue bem-sucedido.

## Manutenibilidade / testes

| ID | Requisito |
|---|---|
| NFR-TEST-01 | Testes unitários dos casos de uso |
| NFR-TEST-02 | PBT das propriedades **P-API-01..04** (Functional Design) |
| NFR-TEST-03 | Testes de API com FastAPI `TestClient` |
| NFR-TEST-04 | `lote-shared` testável de forma isolada (domínio/portas) |

## Usabilidade (API)

| ID | Requisito |
|---|---|
| NFR-UX-01 | OpenAPI/Swagger automático via FastAPI |
| NFR-UX-02 | Mensagens de erro de domínio claras no corpo JSON |

## Fora de escopo deste ciclo (API)

- HA / multi-réplica
- Auth / API keys / TLS
- Prometheus
- Metas de carga além de < 10 req/min

## Conformidade de extensões

| Extensão | Status |
|---|---|
| PBT | Aplicável — NFR-TEST-02 |
| Security Baseline | Disabled — apenas NFR-SEC mínimos acima |
| Resiliency Baseline | Disabled — NFR-REL conforme Q7=B |
