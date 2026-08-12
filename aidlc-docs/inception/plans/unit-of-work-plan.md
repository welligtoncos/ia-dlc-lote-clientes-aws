# Plano de Unidades de Trabalho

**Projeto**: Serviço de Ingestão de Clientes (MVP local)  
**Status**: APPROVED — Inception concluído; projetos Python segregados confirmados.

### Decisões finais
| # | Escolha | Significado |
|---|---|---|
| Q1 | A | 2 unidades: `unit-dominio-api` + `unit-worker-validacao` |
| Q2 | B | Lib compartilhada (`libs/` = projeto `lote-shared`) |
| Q3 | B | Ownership separado API vs Worker |
| Q4 | B | Imagens Docker separadas (mesmo repo) |
| Q5 | B | Dois contextos: Gestão de Lotes + Validação de Qualidade |
| Q6 | B | Pastas `api/` + `worker/` + `libs/` |
| Q7 | A | Construction: API primeiro, depois worker |
| CQ1 | A | Validadores em `libs/` (PBT na lib; API e worker importam) |
| CQ2 | A | Dono da API aprova mudanças em `libs/` |
| **Delta** | User | Cada unidade = **projeto Python isolado** (`pyproject.toml` + venv/lock próprios); sem import cruzado api↔worker |

**Base**: application-design · stories US-01..06 · execution-plan

**Definição**: Unidade de trabalho = agrupamento lógico para desenvolvimento. Imagens Docker **separadas** para api e worker no mesmo repo (Q4=B).

---

## Decisões de decomposição (responda abaixo)

Preencha cada `[Answer]:`. Avise no chat quando terminar.

### Question 1 — Agrupamento de histórias
Como decompor as unidades?

A) **2 unidades**: `unit-dominio-api` (US-01,03,04,05,06 + domain/application/presentation/repo/storage) e `unit-worker-validacao` (US-02 + Celery task + validadores usados pelo worker)

B) **1 unidade monolítica**: toda a aplicação em uma única unit-of-work (módulos lógicos internos apenas)

C) **3 unidades**: `unit-domain-ports`, `unit-api`, `unit-worker` (mais fino; mais coordenação)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 2 — Dependências entre unidades
Como tratar código compartilhado (modelo `Lote`, portas, validadores, repositório)?

A) Pacote `app/` único no monorepo; unit-worker importa os mesmos módulos (sem publicar pacote separado)

B) Extrair biblioteca compartilhada (`app/shared` ou pacote instalável) consumida por api e worker

C) Duplicar contratos mínimos no worker (evitar — só se isolamento extremo)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 3 — Alinhamento da equipe / ownership
Quem “dona” cada unidade neste projeto?

A) Mesma pessoa/time dona de todas as unidades (MVP solo ou time pequeno)

B) Um dono para API/domínio e outro para worker/fila

C) Pairing: qualquer um implementa, mas PRs separados por unidade

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 4 — Considerações técnicas (deploy/escala)
Como as unidades se relacionam à implantação?

A) **Mesma imagem Docker**, dois processos (api e worker) no compose — unidades só lógicas no código

B) Imagens Docker separadas para api e worker (ainda mesmo repo)

C) Serviços implantáveis independentes com repos/pipelines separados (fora do espírito do MVP)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 5 — Domínio de negócio / bounded context
O bounded context é único (“Ingestão de Lotes”)?

A) Sim — um único contexto; unidades são cortes técnicos (API vs Worker), não contextos DDD distintos

B) Dois contextos: “Gestão de Lotes” (CRUD) e “Validação de Qualidade” (worker)

C) Mais contextos (descreva em X)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 6 — Organização de código (greenfield)
Estrutura de diretórios preferida?

A) Repo único com `app/` hexagonal (domain/application/infrastructure/presentation) + `tests/` + `docker-compose.yml` na raiz

B) Repo único com pastas de topo `api/` e `worker/` espelhando as unidades (código compartilhado em `app/` ou `libs/`)

C) Monorepo com packages (`packages/api`, `packages/worker`, `packages/domain`)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

### Question 7 — Ordem de Construction
Sequência de execução das unidades na Construction?

A) Primeiro `unit-dominio-api`, depois `unit-worker-validacao` (worker depende do modelo/portas)

B) Primeiro worker/validação, depois API

C) Paralelo (só faz sentido com 1 unidade ou times separados com contratos congelados)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Esclarecimentos obrigatórios (ambiguidades detectadas)

### Contradição 1: Local dos validadores
Você escolheu **2 unidades** com validadores na `unit-worker-validacao` (Q1=A), mas também **biblioteca compartilhada** (Q2=B). Onde os validadores devem viver no código?

### Clarification Question 1
A) Em `libs/` (ou `app/shared`) — compartilhados; worker e (se preciso) API importam; PBT foca nessa lib

B) Só dentro de `worker/` — API não importa validadores; shared fica só para modelo/portas/repositório

C) Em `libs/` com ownership do time worker (Q3=B); API não chama validação de linha

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Contradição 2: Ownership da lib compartilhada
Com donos separados API vs Worker (Q3=B) e lib compartilhada (Q2=B), quem aprova mudanças em `libs/`?

### Clarification Question 2
A) Dono da API — shared é contrato do domínio/CRUD; worker só consome

B) Dono do Worker — shared prioriza validação/contrato da task; API consome modelo/portas

C) Ambos devem aprovar PRs que tocam `libs/` (CODEOWNERS dual)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Nota sobre Q4=B
Imagens Docker **separadas** para api e worker (mesmo repo) — OK; sobrescreve a preferência do PRD de “imagem única”. Será documentado na geração.

---

## Checklist de Execução (após aprovação do plano)

- [x] 1. Carregar design, histórias e respostas deste plano
- [x] 2. Gerar `unit-of-work.md` (definições + estratégia de organização de código)
- [x] 3. Gerar `unit-of-work-dependency.md`
- [x] 4. Gerar `unit-of-work-story-map.md` (todas as histórias atribuídas)
- [x] 5. Validar limites e dependências
- [x] 6. Atualizar `aidlc-state.md` e `audit.md`

### Artefatos obrigatórios
- [x] unit-of-work.md
- [x] unit-of-work-dependency.md
- [x] unit-of-work-story-map.md

## Hipótese do execution-plan (referência)
- unit-dominio-api + unit-worker-validacao  
Ajuste conforme suas respostas acima.

## Conformidade de extensões
| Extensão | Status | Nota |
|---|---|---|
| Security / Resiliency | Off | N/A |
| PBT | On | Propriedades concentradas na unidade que contém validadores |
