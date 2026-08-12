# Plano de Requisitos NFR — unit-dominio-api

**Status**: Artefatos gerados — aguardando aprovação  

### Decisões
| # | Answer | Resumo |
|---|---|---|
| Q1 | A | p95 POST < 300 ms |
| Q2 | A | < 10 req/min; 1 instância |
| Q3 | A | Best-effort; sem SLA |
| Q4 | A | Secrets via env; sem auth/TLS |
| Q5 | A | FastAPI/Uvicorn/SQLAlchemy2/PyMySQL/Celery/Pydantic2 |
| Q6 | A | Logs JSON stdout |
| Q7 | B | Lote PENDENTE mesmo se broker falhar; 202; reprocessar depois |
| Q8 | A | Unit + PBT P-API-* + TestClient |

## Checklist

- [x] 1. Analisar respostas e gerar `nfr-requirements.md`
- [x] 2. Gerar `tech-stack-decisions.md`
- [x] 3. Atualizar estado e audit
- [ ] 4. Apresentar aprovação → próximo: **NFR Design**

## Extensões
| Extensão | Nota |
|---|---|
| PBT | NFR-TEST-02 |
| Security / Resiliency | Off |
