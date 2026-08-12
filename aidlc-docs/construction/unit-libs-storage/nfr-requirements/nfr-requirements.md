# Requisitos NFR — unit-libs-storage

**Decisões**: Q1–Q9 = A  
**Escopo**: biblioteca de storage (`lote-shared`); plataforma AWS detalhada em `unit-infra-aws`

---

## Desempenho

| ID | Requisito |
|---|---|
| NFR-LIB-PERF-01 | Sem SLO rígido na lib; I/O **síncrono** bloqueante aceitável |
| NFR-LIB-PERF-02 | Objetos até **5 MB** (limite de negócio do produto); lib não impõe compressão |

## Escalabilidade

| ID | Requisito |
|---|---|
| NFR-LIB-SCALE-01 | Adapter **stateless** (estado só em fs/S3) |
| NFR-LIB-SCALE-02 | Um client S3 por instância do adapter; suficiente para `dev` |

## Disponibilidade / resiliência

| ID | Requisito |
|---|---|
| NFR-LIB-AVAIL-01 | **Sem retry interno** na lib; falhas sobem como `ErroArmazenamento` / `ObjetoNaoEncontrado` |
| NFR-LIB-AVAIL-02 | Retries de processamento permanecem no Celery (worker); SDK defaults mínimos ok |

## Segurança

| ID | Requisito |
|---|---|
| NFR-LIB-SEC-01 | Sem credenciais no código; S3 via **default credential chain** |
| NFR-LIB-SEC-02 | Não logar conteúdo do CSV na lib |
| NFR-LIB-SEC-03 | Refs (chaves) podem aparecer em logs de api/worker; lib não exige logger |
| NFR-LIB-SEC-04 | Sanitização agressiva de path (`..`) **não** exigida neste ciclo (Q4=A) — confiar no nome gerado pelo caso de uso |

## Observabilidade

| ID | Requisito |
|---|---|
| NFR-LIB-OBS-01 | Sem métricas embutidas; observabilidade nos consumidores (api/worker) |

## Testes / manutenibilidade

| ID | Requisito |
|---|---|
| NFR-LIB-TEST-01 | Unitários Local + S3 com **moto** (ou equivalente) |
| NFR-LIB-TEST-02 | PBT leve sobre invariantes da ref (não vazia, sem scheme, prefixo `lotes/`) |
| NFR-LIB-TEST-03 | Dependência `boto3` sempre em `lote-shared` (Q7=A) |

## Usabilidade

| ID | Requisito |
|---|---|
| NFR-LIB-UX-01 | N/A (biblioteca sem UI) |

## Alinhamento extensões

| Extensão | Aplicação nesta unit |
|---|---|
| Security Baseline | SEC-01..03; IAM/bucket policy → infra |
| Resiliency Baseline | AVAIL-01 (fail fast); DR/RTO → requisitos globais / infra |
| PBT | TEST-02 |
