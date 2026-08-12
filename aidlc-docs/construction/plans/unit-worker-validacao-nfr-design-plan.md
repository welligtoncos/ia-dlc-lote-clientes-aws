# Plano de Design NFR — unit-worker-validacao

**Status**: Artefatos gerados — aguardando aprovação  

### Decisões finais
| # | Answer | Resumo |
|---|---|---|
| Q1 | A | Celery autoretry 3× 60/120/240 + marcar_erro ao esgotar |
| Q2 | A | acks_late + prefetch_multiplier=1 |
| Q3 | A | Uma escrita MySQL ao final |
| Q4 | A | Settings fail-fast |
| Q5 | A | Componentes: CeleryApp, Task, LeitorCsv, ServicoValidacao, LoteRepo, JsonLogger, Settings (+ CacheInvalidator) |
| Q6 | A | Invalidar cache Valkey DB1 após CONCLUIDO/ERRO |
| Q7 | A | Logs com task_id + lote_id + tentativa |

## Checklist

- [x] 1. Analisar NFR Requirements do worker + padrões da API
- [x] 2. Coletar respostas (questions)
- [x] 3. Gerar `nfr-design-patterns.md`
- [x] 4. Gerar `logical-components.md`
- [x] 5. Atualizar estado/audit
- [ ] 6. Aprovação → próximo: **Infrastructure Design**

## Extensões
| Extensão | Status |
|---|---|
| Resiliency / Security baselines | N/A (disabled) |
| PBT | N/A neste artefato |
