# Plano de Design Funcional — unit-worker-validacao (`lote-worker` + validadores em `lote-shared`)

**Unidade**: unit-worker-validacao  
**Projeto**: `worker/` (`lote-worker`)  
**Histórias**: US-02  
**Status**: Artefatos gerados — aguardando aprovação  
**Escopo**: Lógica de negócio agnóstica a infra

### Decisões
| # | Answer |
|---|---|
| Q1 | A — CPF só 11 dígitos literais (máscara inválida) |
| Q2 | A — linhas em branco ignoradas |
| Q3 | A — cabeçalho inválido → retries → ERRO |
| Q4 | A — só contagens (sem detalhe por linha) |
| Q5 | A — noop se CONCLUIDO + mesmo celery_task_id |
| Q6 | A — retry do zero |
| Q7 | B — PROCESSANDO só após cabeçalho OK |
| Q8 | A — aceitar BOM |
| Q9 | A — PBT validadores + contagem + idempotência |

---

## Checklist de execução

- [x] 1. Carregar unit-of-work, US-02, requirements §6, artefatos da API e stubs atuais
- [x] 2. Coletar respostas às perguntas (arquivo de questions)
- [x] 3. Resolver ambiguidades / follow-ups se necessário
- [x] 4. Gerar `business-logic-model.md`
- [x] 5. Gerar `business-rules.md`
- [x] 6. Gerar `domain-entities.md`
- [x] 7. Incluir seção **Propriedades Testáveis (PBT)** (PBT-01) — P-VAL-01..07
- [x] 8. Atualizar `aidlc-state.md` e `audit.md`

### Artefatos
- [x] business-logic-model.md
- [x] business-rules.md
- [x] domain-entities.md

## Extensões — conformidade
| Regra | Status | Nota |
|---|---|---|
| PBT-01 | Compliant | P-VAL-01..07 documentadas |
| PBT-02.. | N/A neste estágio | Detalhe na geração de código |
| Security / Resiliency | N/A | Disabled |
