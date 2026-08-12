# Plano de Design Funcional — unit-dominio-api (`lote-api` + ownership `lote-shared`)

**Unidade**: unit-dominio-api  
**Histórias**: US-01, US-03, US-04, US-05, US-06  
**Status**: Artefatos gerados — aguardando aprovação  
**Escopo**: Lógica de negócio agnóstica a infra

### Decisões
| # | Answer |
|---|---|
| Q1–Q8 | A |

---

## Checklist de execução

- [x] 1. Carregar unit-of-work, stories, requirements e respostas
- [x] 2. Gerar `business-logic-model.md`
- [x] 3. Gerar `business-rules.md`
- [x] 4. Gerar `domain-entities.md`
- [x] 5. Incluir seção **Propriedades Testáveis (PBT)** aplicáveis a esta unidade (PBT-01)
- [x] 6. Atualizar `aidlc-state.md` e `audit.md`

### Artefatos
- [x] business-logic-model.md
- [x] business-rules.md
- [x] domain-entities.md

## Extensões — conformidade
| Regra | Status | Nota |
|---|---|---|
| PBT-01 | Compliant | P-API-01..04 documentadas; validadores de linha adiados (Q7=A) |
| PBT-02.. | N/A neste estágio | Detalhe na geração de código / unit-worker |
| Security / Resiliency | N/A | Disabled |
