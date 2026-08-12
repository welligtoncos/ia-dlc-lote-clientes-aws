# Plano — Design Funcional: unit-worker-s3

**Unidade**: `unit-worker-s3` (`worker/` / `lote-worker`)  
**História**: US-AWS-03 (+ regressão US-AWS-04 fs)  
**Depende de**: libs storage (`abrir`), api dual kwargs  

---

## Checklist (após respostas)

- [x] Gerar `business-logic-model.md`
- [x] Gerar `business-rules.md`
- [x] Gerar `domain-entities.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Assinatura da task `ingerir_clientes`

A) Aceitar **ambos**: `caminho=` (fs) **ou** `bucket=`+`chave=` (s3); exatamente um modo por chamada

B) Só S3 neste ciclo (quebrar Compose até mudar api local)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Como obter bytes do CSV

A) Usar `PortaArmazenamentoArquivo.abrir(ref)` da lib (factory fs/s3); processador não chama boto3 direto

B) boto3 só no worker, bypass da porta

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Leitura CSV a partir de bytes

A) Evoluir `ler_csv_clientes` para aceitar path **ou** `bytes`/`TextIO` (ex.: `ler_csv_clientes_de_bytes`)

B) Sempre gravar tempfile e reusar leitor path-only

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4 — Credenciais S3 no worker

A) Default credential chain / task role; **não** exigir ACCESS_KEY no worker se role existir (ECS); Compose fs sem S3

B) Mesma regra da API (Q6=B): sempre exigir ACCESS_KEY se backend s3

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 5 — Retry / regras de negócio de validação

A) Manter retry 60/120/240, idempotência CONCLUIDO, validadores Fase 1 — só muda origem do arquivo

B) Alterar política de retry neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Aprovar e gerar

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
