# Plano de Design de Infraestrutura — unit-dominio-api

**Status**: Artefatos gerados — aguardando aprovação  

### Decisões finais
| # | Answer | Resumo |
|---|---|---|
| Q1 | B | Compose local + esboço Terraform/Copilot (sem apply) |
| Q2 | A | Container api, Uvicorn 1 worker, :8000 |
| Q3 | A | mysql:8 + volume `lotes_files` |
| Q4 | A | Valkey DB0 broker / DB1 cache |
| Q5 | A | 8000:8000 direto |
| Q6 | A | docker logs + /health |
| Q7 | C→**CQ1=A** | Compose **raiz único** (projetos Python separados) |

## Checklist

- [x] 1. Gerar `infrastructure-design.md`
- [x] 2. Gerar `deployment-architecture.md`
- [x] 3. Gerar `shared-infrastructure.md`
- [x] 4. Atualizar estado/audit
- [ ] 5. Aprovação → próximo: **Code Generation**

## Extensões
| Extensão | Status |
|---|---|
| Security / Resiliency / PBT | N/A neste estágio |
