# Plano de Design NFR — unit-dominio-api

**Status**: Artefatos gerados — aguardando aprovação  

### Decisões finais
| # | Answer | Resumo |
|---|---|---|
| Q1 | A | Degraded enqueue (try/except) |
| Q2 | C | Cache-aside Valkey nos GET (confirmado CQ1=A) |
| Q3 | A | Fast path upload sem parse |
| Q4 | B | Settings + fail-fast env |
| Q5 | A | MW log + Settings + pools + Celery wrapper + /health |
| Q6 | A | request_id + X-Request-ID |
| CQ1 | A | Manter cache Valkey no MVP |

## Checklist

- [x] 1. Gerar `nfr-design-patterns.md`
- [x] 2. Gerar `logical-components.md`
- [x] 3. Atualizar estado/audit
- [ ] 4. Aprovação → próximo: **Infrastructure Design**

## Extensões
| Extensão | Status |
|---|---|
| Resiliency / Security baselines | N/A (disabled) |
| PBT | N/A neste artefato |
