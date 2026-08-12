# Personas — Serviço de Ingestão de Clientes

**Base**: requirements.md + plano aprovado (Q4=B)

---

## P1 — Integrador (sistema / script)

| Campo | Descrição |
|---|---|
| **Papel** | Sistema externo ou script que envia lotes de clientes |
| **Objetivo** | Enviar CSV e obter imediatamente um identificador para acompanhar o processamento |
| **Motivações** | Automatizar ingestão em lote; não bloquear o pipeline de integração |
| **Dores** | Timeouts em APIs síncronas; falta de rastreabilidade do arquivo enviado |
| **Comportamento** | Chama `POST /lotes`, guarda `lote_id`/`task_id`, consulta status depois |
| **Histórias** | US-01 |

---

## P2 — Analista de dados

| Campo | Descrição |
|---|---|
| **Papel** | Profissional que avalia qualidade dos cadastros recebidos |
| **Objetivo** | Ver quantos registros foram válidos/inválidos por lote e listar ingestões |
| **Motivações** | Qualidade de dados; auditoria simples do histórico de lotes |
| **Dores** | Não saber a procedência/resultado de um arquivo; métricas espalhadas |
| **Comportamento** | Usa `GET /lotes` e `GET /lotes/{id}` |
| **Histórias** | US-03, US-04 |

---

## P3 — Operador

| Campo | Descrição |
|---|---|
| **Papel** | Operação responsável por recuperar falhas e limpar registros |
| **Objetivo** | Reprocessar lotes com erro e remover ingestões antigas do banco |
| **Motivações** | Restaurar processamento sem recriar lote do zero; higiene do catálogo |
| **Dores** | Lotes “presos” ou falhos sem caminho de recuperação; acúmulo de registros |
| **Comportamento** | Usa `PUT /lotes/{id}` (só `ERRO`) e `DELETE /lotes/{id}` |
| **Histórias** | US-05, US-06 |

---

## P4 — Worker / Sistema (persona técnica)

| Campo | Descrição |
|---|---|
| **Papel** | Processo Celery que consome a fila e valida o CSV |
| **Objetivo** | Processar o arquivo no volume compartilhado, validar linhas e persistir resumo |
| **Motivações** | Desacoplar API do trabalho pesado; garantir status durável no MySQL |
| **Dores** | Falhas transitórias (I/O, banco); risco de reexecução duplicada |
| **Comportamento** | Consome task allowlisted, atualiza `PENDENTE→PROCESSANDO→CONCLUIDO|ERRO`, aplica retry/idempotência |
| **Histórias** | US-02 |

---

## Mapa Persona → Histórias

| Persona | Must |
|---|---|
| P1 Integrador | US-01 |
| P4 Worker | US-02 |
| P2 Analista | US-03, US-04 |
| P3 Operador | US-05, US-06 |
