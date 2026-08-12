# Requisitos NFR — unit-worker-validacao

**Unidade**: unit-worker-validacao (`lote-worker` + validadores em `lote-shared`)  
**Decisões**: Q1=A, **Q2=B**, Q3=A, Q4=A, Q5=A, Q6=A, Q7=A, Q8=A

---

## Desempenho

| ID | Requisito |
|---|---|
| NFR-PERF-W01 | Processamento de CSV ≤ 5 MB: **best-effort** — sem SLO formal; conclusão em minutos é aceitável no MVP local (Q1=A) |
| NFR-PERF-W02 | Parsing em **streaming** (stdlib `csv`) para evitar carregar o arquivo inteiro em memória desnecessariamente (Q3=A) |

## Escalabilidade

| ID | Requisito |
|---|---|
| NFR-SCALE-W01 | Compose MVP: **1** processo worker Celery com **`concurrency=2`** (até 2 lotes em paralelo) (Q2=B) |
| NFR-SCALE-W02 | Escala horizontal futura por réplicas de container worker (não exigida neste ciclo); API e worker escalam independentemente (RNF-02) |
| NFR-SCALE-W03 | Sem teto adicional de linhas além do limite de 5 MB da API (Q6=A) |

## Disponibilidade

| ID | Requisito |
|---|---|
| NFR-AVAIL-W01 | Best-effort (dev/demo): **sem SLA** |
| NFR-AVAIL-W02 | Recuperação: restart do serviço `worker` / `docker compose` |

## Confiabilidade

| ID | Requisito |
|---|---|
| NFR-REL-W01 | Retry Celery: até **3** tentativas, backoff **60s / 120s / 240s**; depois lote `ERRO` (RNF-03 / FD) |
| NFR-REL-W02 | Retry **recomeça do zero** (releitura completa); sem checkpoint por linha |
| NFR-REL-W03 | Idempotência: no-op se `CONCLUIDO` + mesmo `celery_task_id` |
| NFR-REL-W04 | Status/resumo canônicos no **MySQL** (não result backend Celery) (Q7=A; RNF-08) |
| NFR-REL-W05 | Sem soft/hard time limit explícito da task no MVP (Q5=A) |

## Segurança (MVP)

| ID | Requisito |
|---|---|
| NFR-SEC-W01 | Credenciais / URLs só via variáveis de ambiente |
| NFR-SEC-W02 | Sem auth na fila neste ciclo (rede compose local) |
| NFR-SEC-W03 | Worker não expõe porta HTTP |

## Observabilidade

| ID | Requisito |
|---|---|
| NFR-OBS-W01 | Logs **JSON** em stdout (Q4=A) |
| NFR-OBS-W02 | Campos mínimos: `lote_id`, `task_id`, `tentativa`, `duracao_ms`, `status_final` (CONCLUIDO/ERRO/NOOP), mensagem de erro se houver |
| NFR-OBS-W03 | Sem Prometheus neste ciclo |

## Manutenibilidade / testes

| ID | Requisito |
|---|---|
| NFR-TEST-W01 | Testes unitários da lógica da task / orquestração |
| NFR-TEST-W02 | PBT **P-VAL-01..07** em `lote-shared` (validadores + invariante + idempotência documentada) |
| NFR-TEST-W03 | Teste de integração leve: task com repositório/arquivo **fake** (Q8=A) |
| NFR-TEST-W04 | Projeto `lote-worker` isolado: sem dependência de `lote-api` |

## Usabilidade operacional

| ID | Requisito |
|---|---|
| NFR-OPS-W01 | Serviço `worker` no `docker-compose` com comando Celery documentado |
| NFR-OPS-W02 | Mesmo volume `lotes_files` e MySQL/Valkey da API |

## Fora de escopo deste ciclo (worker)

- SLO formal de latência de processamento
- Result backend Redis/Celery
- pandas
- Prometheus / APM
- Time limits soft/hard
- Teto de linhas além de 5 MB

## Conformidade de extensões

| Extensão | Status |
|---|---|
| PBT | Aplicável — NFR-TEST-W02 |
| Security Baseline | Disabled — NFR-SEC-W* mínimos |
| Resiliency Baseline | Disabled — NFR-REL-W* do produto |
