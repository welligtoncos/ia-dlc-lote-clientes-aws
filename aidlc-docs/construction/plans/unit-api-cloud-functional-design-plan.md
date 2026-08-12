# Plano — Design Funcional: unit-api-cloud

**Unidade**: `unit-api-cloud` (`api/` / `lote-api`)  
**Histórias**: US-AWS-01 (app ready), US-AWS-02, US-AWS-04  
**Depende de**: `unit-libs-storage` (porta + factory)  
**Foco**: enqueue Celery dual kwargs; composition já parcial; **sem** validar API Key na app

---

## Checklist (após respostas)

- [x] Gerar `business-logic-model.md`
- [x] Gerar `business-rules.md`
- [x] Gerar `domain-entities.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Onde montar kwargs da task (fs vs s3)

A) **Só no AdaptadorCelery** (infra): caso de uso passa `{lote_id, ref}`; adapter traduz para `{lote_id, caminho}` ou `{lote_id, bucket, chave}` conforme `STORAGE_BACKEND` (App Design Q3=A)

B) Caso de uso monta kwargs tipados conhecendo o backend

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Como o adapter obtém `bucket` na cloud

A) Env/`Configuracoes.s3_bucket` injetado no AdaptadorCelery; `chave` = ref relativa

B) Parsear URI da ref (exigiria mudar formato da ref)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Campo `caminho` no payload fs

A) Manter nome `caminho` = ref relativa (worker resolve com `STORAGE_LOCAL_DIR`) — compatível com worker atual pós-libs

B) Renomear para `ref` nos kwargs fs (breaking worker até unit-worker-s3)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Reprocessar lote

A) Mesma tradução: re-enfileira com a `ref` já em `lote.caminho_arquivo` via adapter

B) Lógica especial diferente do ingest

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — API Key / US-AWS-01 na api

A) Nenhuma mudança de auth na FastAPI (Gateway na unit-infra); garantir contrato HTTP/202 inalterado

B) Middleware opcional de API Key na api (flag env)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Health check

A) Manter health atual; liberação no Gateway é infra

B) Adicionar `/health` público documentado se ainda não existir

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Aprovar e gerar design funcional

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
