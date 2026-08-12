# Plano de Requisitos NFR — unit-worker-validacao

**Status**: Artefatos gerados — aguardando aprovação  

### Decisões
| # | Answer | Resumo |
|---|---|---|
| Q1 | A | Best-effort; sem SLO formal |
| Q2 | B | concurrency=2 |
| Q3 | A | stdlib `csv` streaming |
| Q4 | A | Logs JSON stdout |
| Q5 | A | Sem soft/hard time limit |
| Q6 | A | Sem teto extra de linhas |
| Q7 | A | Celery+shared+pytest; sem result backend; sem FastAPI |
| Q8 | A | Unit + PBT P-VAL + integração leve |

## Checklist

- [x] 1. Analisar Functional Design do worker + NFR da API
- [x] 2. Coletar respostas NFR (questions)
- [x] 3. Gerar `nfr-requirements.md`
- [x] 4. Gerar `tech-stack-decisions.md`
- [x] 5. Atualizar estado e audit
- [ ] 6. Apresentar aprovação → próximo: **NFR Design**

## Extensões
| Extensão | Nota |
|---|---|
| PBT | NFR-TEST-W02 |
| Security / Resiliency | Off |
