# Plano de Design da Aplicação

**Projeto**: Serviço de Ingestão de Clientes (MVP local)  
**Status**: Artefatos gerados — aguardando aprovação  
**Base**: requirements.md · stories.md · execution-plan.md

### Decisões capturadas
| # | Escolha | Significado |
|---|---|---|
| Q1 | A | 4 camadas hexagonais |
| Q2 | B | Validação na Application (pura / PBT) |
| Q3 | A | PortaLoteRepositorio no Domain |
| Q4 | A | Um caso de uso por endpoint |
| Q5 | A | PortaArmazenamentoArquivo |
| Q6 | A | Assinaturas + propósito curto |

---

## Respostas

### Question 1 — Limites dos componentes
[Answer]: A

### Question 2 — Onde vive a validação de linhas do CSV?
[Answer]: B

### Question 3 — Porta de persistência
[Answer]: A

### Question 4 — Orquestração dos casos de uso
[Answer]: A

### Question 5 — Armazenamento do arquivo no design
[Answer]: A

### Question 6 — Nível de detalhe dos métodos neste estágio
[Answer]: A

---

## Checklist de Execução

- [x] 1. Carregar requisitos, histórias e respostas deste plano
- [x] 2. Gerar `components.md`
- [x] 3. Gerar `component-methods.md`
- [x] 4. Gerar `services.md`
- [x] 5. Gerar `component-dependency.md`
- [x] 6. Gerar `application-design.md` (consolidado)
- [x] 7. Validar consistência (portas, dependências, histórias US-01..06)
- [x] 8. Atualizar `aidlc-state.md` e `audit.md`

### Artefatos obrigatórios
- [x] components.md
- [x] component-methods.md
- [x] services.md
- [x] component-dependency.md
- [x] application-design.md

## Conformidade de extensões
| Extensão | Status | Neste estágio |
|---|---|---|
| Security | Disabled | N/A |
| Resiliency | Disabled | N/A |
| PBT | Enabled | Validadores na Application como funções puras (Q2=B) |
