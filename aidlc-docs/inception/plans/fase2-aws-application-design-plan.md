# Plano — Design da Aplicação Fase 2 (Migração AWS)

**Requisitos**: `fase2-aws-requirements.md`  
**Histórias**: `fase2-aws-stories.md`  
**As-is**: hexagonal C1–C4 em `application-design/` (Fase 1)  
**Escopo deste design**: deltas de componentes/serviços para S3, kwargs task, dual backend, limites cloud (Gateway auth no edge)

---

## Checklist de geração (após aprovação do plano)

- [x] `aidlc-docs/inception/application-design/fase2-aws-components.md`
- [x] `aidlc-docs/inception/application-design/fase2-aws-component-methods.md`
- [x] `aidlc-docs/inception/application-design/fase2-aws-services.md`
- [x] `aidlc-docs/inception/application-design/fase2-aws-component-dependency.md`
- [x] `aidlc-docs/inception/application-design/fase2-aws-application-design.md` (consolidado)
- [x] Validar consistência com RF-AWS / US-AWS e hexagonal existente
- [x] Não sobrescrever artefatos Fase 1 em `components.md` etc.

---

# Perguntas — preencha cada `[Answer]:`

## Question 1
Onde vive o adapter S3 e a fábrica de storage?

A) Em `libs` (`lote-shared`): `ArmazenamentoArquivoS3` + factory por `STORAGE_BACKEND`; api e worker só consomem a porta

B) Adapter S3 só na `api` (upload); worker com cliente S3 próprio (duplicação aceitável neste ciclo)

C) Pacote novo `libs/cloud` separado de `lote-shared`

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2
A porta `PortaArmazenamentoArquivo` na Domain?

A) Manter assinatura lógica atual; S3 implementa a mesma porta (salvar/abrir por referência — path local ou `s3://bucket/chave` / tuple)

B) Evoluir a porta: métodos explícitos `salvar_objeto(bucket, chave, bytes)` / `abrir_objeto(bucket, chave)` além do filesystem

C) Duas portas: `PortaArmazenamentoLocal` e `PortaArmazenamentoObjeto` selecionadas na Application

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3
Como a Application monta kwargs da task na cloud?

A) Application recebe referência opaca do storage (`ref`) e o AdaptadorCelery/infra traduz para `{lote_id, bucket, chave}` ou `{lote_id, caminho}` conforme backend

B) Application conhece `bucket`/`chave` quando `STORAGE_BACKEND=s3` e passa kwargs tipados à porta de tarefa

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4
API Key / autenticação no design de componentes da aplicação?

A) Fora da app: só API Gateway; Presentation FastAPI **não** valida API Key (confiança na rede privada ALB↔ECS)

B) Defesa em profundidade: Gateway **e** middleware opcional na API (flag env)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5
Terraform / GHA no Design da Aplicação?

A) Fora deste estágio — apenas fronteiras (env, IAM roles esperadas, outputs); detalhe em Infrastructure Design / Units

B) Incluir componentes lógicos “InfraProvisioning” e “CiCdPipeline” nos artefatos de application-design

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6
Padrão de seleção `STORAGE_BACKEND`?

A) Factory no composition root (api `main` / worker bootstrap) — Application permanece agnóstica

B) Service locator / DI container novo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7
Aprova este plano de design (gerar artefatos após Q1–Q6)?

A) Aprovar — gerar design conforme respostas

B) Solicitar alterações no plano (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
