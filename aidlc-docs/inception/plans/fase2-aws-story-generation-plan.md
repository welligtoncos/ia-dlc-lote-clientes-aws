# Plano de Geração de Histórias — Fase 2 Migração AWS

**Estágio**: INCEPTION — User Stories (Parte 1: Planejamento)  
**Requisitos**: `aidlc-docs/inception/requirements/fase2-aws-requirements.md`  
**Histórias Fase 1 (referência)**: `aidlc-docs/inception/user-stories/stories.md`  
**Assessment**: `aidlc-docs/inception/plans/fase2-aws-user-stories-assessment.md`

---

## Checklist de execução (após aprovação deste plano)

- [x] Gerar `aidlc-docs/inception/user-stories/fase2-aws-personas.md`
- [x] Gerar `aidlc-docs/inception/user-stories/fase2-aws-stories.md` (INVEST + AC)
- [x] Mapear personas ↔ histórias
- [x] Mapear histórias ↔ RF-AWS / RNF-AWS
- [x] Não reescrever histórias MVP Fase 1; referenciar US-01..06 onde o comportamento funcional permanece
- [x] Validar conformidade INVEST e critérios de aceite testáveis

---

## Abordagens de decomposição (trade-offs)

| Abordagem | Benefício | Risco |
|---|---|---|
| **Jornada** | Fluxo Integrador → Gateway → S3 → Worker → GET | Pode misturar infra e app |
| **Funcionalidade** | Agrupa por capacidade (auth, storage, deploy) — alinhado Fase 1 | Menos narrativa de ponta a ponta |
| **Persona** | Clara por papel (Integrador vs DevOps) | Duplicação entre papéis |
| **Domínio** | App vs Infra vs Ops | Fronteiras artificiais |
| **Epic** | Epics AWS com sub-histórias | Overhead se escopo já fechado |

**Recomendação sugerida**: híbrido **Funcionalidade + Persona** (como Fase 1), com 1 epic leve “Migração AWS” se Q1=E.

---

## Escopo das histórias Fase 2 (proposta)

Foco em **deltas** da migração (não recontar todo o MVP):

1. Autenticar e chamar API via Gateway (API Key)
2. Upload com persistência S3 + kwargs `{lote_id, bucket, chave}`
3. Worker ECS consumindo S3 e atualizando RDS
4. Manter Compose local com filesystem
5. Provisionar/aplicar stack Terraform em `dev` via GHA
6. Dump/restore MySQL → RDS
7. Smoke pós-deploy + rollback note (change management leve)

---

# Perguntas — responda cada `[Answer]:`

## Question 1
Abordagem de decomposição das histórias Fase 2?

A) Por funcionalidade (auth Gateway, storage S3, worker ECS, Terraform/CI, dump/restore, Compose)

B) Por jornada ponta a ponta (poucas histórias longas: “enviar lote na cloud”, “operar deploy”)

C) Por persona (bloco Integrador, bloco DevOps, bloco Analista)

D) Epic “Migração AWS” com sub-histórias numeradas

E) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2
Granularidade?

A) Fina — 1 história por RF-AWS principal (~10–14 histórias)

B) Média — agrupar RF relacionados (~6–8 histórias) — recomendado

C) Grossa — 3–4 histórias épicas apenas

D) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 3
Formato dos critérios de aceitação?

A) Só Gherkin

B) Só bullets/checklists

C) Híbrido: Gherkin nos fluxos principais + bullets em ops/infra (como Fase 1)

D) Outro (descreva após [Answer]:)

[Answer]: C

---

## Question 4
Personas Fase 2?

A) Reusar P1–P4 da Fase 1 e **adicionar P5 DevOps/Cloud** (Terraform, GHA, dump/restore, smoke)

B) Só personas novas focadas em cloud (Integrador-cloud + DevOps); omitir Analista/Worker se sem delta

C) Expandir P3 Operador para incluir cloud (sem P5 separado)

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5
Histórias do MVP local (US-01..06) na documentação Fase 2?

A) Manter arquivos Fase 1 intactos; Fase 2 só em `fase2-aws-stories.md` com links/referências aos US que não mudam

B) Reescrever um único `stories.md` unificado (Fase 1 + deltas AWS)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6
Priorização das histórias Fase 2?

A) MoSCoW (Must = escopo deste ciclo; Should/Could explícitos se houver)

B) Ordem numérica apenas (todas Must implícito pelo escopo do ciclo)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7
Incluir história explícita de **change management leve** (PR/GHA + nota de rollback — CQ4=B)?

A) Sim — história Must para DevOps (runbook + trilha PR)

B) Não — cobrir só como AC dentro da história de CI/CD Terraform

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8
Incluir história de **segurança** (API Key, S3 privado, secrets) separada?

A) Sim — história Must focada em controles Security Baseline visíveis ao usuário/ops

B) Não — espalhar AC de segurança nas histórias de Gateway, S3 e Terraform

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Aprovação do plano (após responder Q1–Q8)

Preencha após responder as perguntas acima:

## Question 9
Aprova este plano de geração de histórias?

A) Aprovar — gerar personas e histórias conforme respostas

B) Solicitar alterações no plano (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
