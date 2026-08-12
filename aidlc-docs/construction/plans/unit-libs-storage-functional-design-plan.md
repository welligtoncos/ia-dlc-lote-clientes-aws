# Plano — Design Funcional: unit-libs-storage

**Unidade**: `unit-libs-storage` (`libs/` / `lote-shared`)  
**Histórias**: US-AWS-02, US-AWS-04  
**Foco**: regras de negócio do storage dual (fs/s3), formato da referência opaca, factory — **agnóstico de Terraform/IAM**

---

## Checklist (após respostas + aprovação implícita via Qn)

- [x] Gerar `business-logic-model.md`
- [x] Gerar `business-rules.md`
- [x] Gerar `domain-entities.md`
- [x] Validar alinhamento com porta `PortaArmazenamentoArquivo` e App Design Fase 2

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Formato da referência opaca retornada por `salvar`

A) **Chave/path relativo apenas** (ex.: `lotes/123_arquivo.csv`); bucket/base dir ficam na config do adapter

B) **URI completa** (ex.: `s3://bucket/lotes/...` ou `file:///data/...`)

C) **Prefixed scheme** curto: `s3:chave` / `fs:caminho` no mesmo string

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Convenção de nome do objeto/arquivo

A) Manter Fase 1: `{lote_id}_{nome_original}` sob prefixo `lotes/` no S3 (e dir base no fs)

B) UUID + extensão; `lote_id` só no banco

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Onde vive `ArmazenamentoArquivoLocal` hoje (pode estar na api)

A) **Mover/consolidar na libs** neste unit (api/worker importam só da lib)

B) Deixar Local na api; libs só adiciona S3 + factory que instancia Local via callback/path config

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Comportamento de `existe(ref)`

A) fs: `Path.exists`; s3: `head_object` (404 → False; outros erros → propagar)

B) Ambos retornam False em qualquer falha (nunca levantam)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Erros de negócio do storage (exceções de domínio na lib)

A) Introduzir `ErroArmazenamento` / `ObjetoNaoEncontrado` na lib para falhas de I/O relevantes

B) Deixar exceções técnicas do SDK/OS subirem; casos de uso tratam depois

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Factory `criar_armazenamento`

A) Valores: `fs` (default) e `s3`; backend desconhecido → erro explícito na factory

B) Aceitar aliases (`filesystem`, `local`, `S3`) normalizados

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7 — Leitura do conteúdo (worker precisa do CSV)

A) Estender porta com `abrir(ref) -> bytes|BinaryIO` neste unit (necessário para worker sem acoplar boto3)

B) Porta só `salvar`/`existe`; leitura S3 fica só no worker (fora desta unit)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 8 — Aprovar e gerar design funcional

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações no plano (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
