# Perguntas — Design Funcional unit-worker-validacao

Responda cada pergunta preenchendo `[Answer]:` com a letra (ex.: `A`) ou descreva em `X) Outro`.

---

## Question 1
Para **CPF**, o requirements exige 11 dígitos + dígito verificador, sem normalização automática. Como tratar entrada com máscara (`529.982.247-25`)?

A) Aceitar apenas string com exatamente 11 caracteres numéricos (máscara = inválido)

B) Extrair dígitos só para validar DV (máscara com 11 dígitos válidos = linha válida); **não** persistir valor normalizado (só contagens)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 2
Linhas **em branco** ou só com espaços no CSV (após o cabeçalho): como contar?

A) Ignorar (não entram em `total_linhas`)

B) Contar em `total_linhas` e em `linhas_invalidas`

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 3
Se o **cabeçalho** estiver ausente, incompleto ou diferente de `nome,email,cpf,telefone` (UTF-8, `,`):

A) Falha de processamento → após retries → lote `ERRO` (não gera resumo de linhas)

B) Lote `CONCLUIDO` com `total_linhas=0` e mensagem em `erro` (sem retries de negócio)

C) Tratar todas as linhas de dados como inválidas e ainda assim `CONCLUIDO` com contagens

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 4
Além das **contagens** no MySQL, o worker deve persistir **detalhe** das linhas inválidas (motivo / número da linha)?

A) Não — apenas contagens + status (MVP)

B) Sim — arquivo sidecar (ex.: `{lote_id}_erros.json`) no volume

C) Sim — tabela MySQL de erros por linha

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 5
**Idempotência** quando a mesma task é reentregue (RF-15):

A) Se o lote já está `CONCLUIDO` **e** `celery_task_id` da mensagem coincide com o do lote → no-op (não reprocessa)

B) Se o lote já está `CONCLUIDO` (qualquer `celery_task_id`) → no-op

C) Sempre reprocessa o CSV e sobrescreve contagens (idempotência só via Celery ack)

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 6
Falha **transitória** no meio do arquivo (ex.: MySQL indisponível após ler metade):

A) Abortar tentativa; no retry **recomeçar do zero** (reler CSV inteiro; contagens finais só no commit de sucesso)

B) Tentar checkpoint por linha (mais complexo)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 7
Quando marcar `PROCESSANDO`?

A) No **início** da execução da task, antes de ler o CSV

B) Somente após validar cabeçalho com sucesso

C) Outro (descreva após [Answer]:)

[Answer]: B

---

## Question 8
UTF-8 com **BOM** no início do arquivo:

A) Aceitar BOM e tratar cabeçalho como válido se as colunas baterem

B) BOM torna o cabeçalho inválido → mesmo tratamento da Q3

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question 9 (PBT)
Propriedades prioritárias para documentar neste Functional Design (além do invariante `total = válidas + inválidas`):

A) Validade isolada de `cpf` (DV), `email`, `telefone`, `nome` + invariante de contagem + no-op idempotente

B) Somente invariante de contagem neste estágio; validadores só com testes de exemplo

C) Outro (descreva após [Answer]:)

[Answer]: A
