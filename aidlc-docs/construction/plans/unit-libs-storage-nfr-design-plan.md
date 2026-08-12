# Plano — NFR Design: unit-libs-storage

**Base**: `nfr-requirements.md` + `tech-stack-decisions.md` (Q1–Q9=A)  
**Foco**: padrões lógicos na lib (não Terraform)

---

## Checklist (após respostas)

- [x] Gerar `nfr-design-patterns.md`
- [x] Gerar `logical-components.md`

---

# Perguntas — preencha cada `[Answer]:`

## Question 1 — Resiliência (padrão de falha)

A) **Fail-fast**: mapear erros SDK/OS → `ErroArmazenamento` / `ObjetoNaoEncontrado`; sem circuit breaker na lib

B) Circuit breaker leve em torno do client S3

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2 — Escalabilidade

A) Instância do adapter por processo (api/worker); sem registry global

B) Singleton de client S3 no módulo (global)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3 — Desempenho

A) Streaming **não** obrigatório: `read`/`write` de bytes completos (≤ 5 MB)

B) Usar upload/download multipart/streaming já neste ciclo

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 4 — Segurança (padrões na lib)

A) Credential chain apenas; validar config obrigatória (bucket) na construção do adapter S3

B) Além de A: interface para injetar client mockável (facilita testes e evita side effects)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5 — Componentes lógicos

A) Três peças: `ArmazenamentoArquivoLocal`, `ArmazenamentoArquivoS3`, `criar_armazenamento` (+ helper de chave `lotes/`)

B) Quarto componente: `ReferenciaArmazenamento` como classe tipada (não só str)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6 — Aprovar e gerar design NFR

A) Aprovar — gerar artefatos conforme respostas

B) Solicitar alterações (descreva após [Answer]:)

C) Outro (descreva após [Answer]:)

[Answer]: A
