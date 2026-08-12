# Plano de Geração de Histórias de Usuário

**Projeto**: Serviço de Ingestão de Clientes (MVP local)  
**Base**: `requirements.md` + PRD  
**Status**: Parte 2 executada — aguardando aprovação das histórias geradas

### Decisões capturadas
| # | Escolha | Significado |
|---|---|---|
| Q1 | B | Decomposição por **funcionalidade** |
| Q2 | B | Granularidade **média** (UC-01..05 + validação/worker se necessário) |
| Q3 | C | AC em **Gherkin** (fluxos) + **bullets** (validação/edge) |
| Q4 | B | Personas: Integrador, Analista, Operador + **Worker/Sistema** |
| Q5 | A | Erros como **AC negativos** nas histórias principais |
| Q6 | A | Priorização **MoSCoW** (Must = UC-01..05 + validação) |

---

## Parte 1 — Decisões de Metodologia (concluída)

### Question 1 — Abordagem de decomposição
[Answer]: B

### Question 2 — Granularidade
[Answer]: B

### Question 3 — Critérios de aceitação
[Answer]: C

### Question 4 — Escopo das personas
[Answer]: B

### Question 5 — Histórias de erro e edge cases
[Answer]: A

### Question 6 — Prioridade relativa (sem sprint planning)
[Answer]: A

---

## Parte 2 — Checklist de Execução

- [x] 1. Carregar `requirements.md` e decisões deste plano
- [x] 2. Gerar `aidlc-docs/inception/user-stories/personas.md`
- [x] 3. Gerar `aidlc-docs/inception/user-stories/stories.md` com histórias INVEST
- [x] 4. Incluir critérios de aceitação no formato aprovado (Q3)
- [x] 5. Mapear cada história → persona(s) e RF/UC relacionados
- [x] 6. Incluir cenários de erro conforme Q5
- [x] 7. Aplicar priorização conforme Q6
- [x] 8. Revisar conformidade INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [x] 9. Atualizar `aidlc-state.md` e `audit.md`

### Artefatos obrigatórios
- [x] `personas.md`
- [x] `stories.md`

---

## Conformidade de extensões (planejamento)
| Extensão | Status | No planejamento de histórias |
|---|---|---|
| Security Baseline | Disabled | N/A |
| Resiliency Baseline | Disabled | N/A |
| Property-Based Testing | Enabled | Histórias de validação devem ser testáveis; propriedades PBT detalhadas no Design Funcional |
