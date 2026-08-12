# Plano de Design de Infraestrutura — unit-worker-validacao

**Status**: Artefatos gerados — aguardando aprovação  

### Decisões finais
| # | Answer | Resumo |
|---|---|---|
| Q1 | A | Worker no compose raiz; AWS só esboço |
| Q2 | A | `celery -A lote_worker.celery_app worker --concurrency=2` |
| Q3 | A | Volume `/data/lotes` RW (worker lê) |
| Q4 | A | Broker DB0 + CACHE_URL DB1 |
| Q5 | A | Sem portas publicadas |
| Q6 | A | Só docker logs; sem Flower |
| Q7 | A | depends_on mysql healthy + valkey |

## Checklist

- [x] 1. Analisar NFR Design worker + shared-infrastructure + compose atual
- [x] 2. Coletar respostas (questions)
- [x] 3. Gerar `infrastructure-design.md`
- [x] 4. Gerar `deployment-architecture.md`
- [x] 5. Atualizar `shared-infrastructure.md` (worker + CACHE_URL)
- [x] 6. Atualizar estado/audit
- [ ] 7. Aprovação → próximo: **Code Generation**

## Extensões
| Extensão | Status |
|---|---|
| Security / Resiliency / PBT | N/A neste estágio |
