# Histórias de Usuário — Serviço de Ingestão de Clientes

**Organização**: por funcionalidade (Q1=B)  
**Granularidade**: média — UC + validação/worker (Q2=B)  
**AC**: Gherkin nos fluxos + bullets em validação/edge (Q3=C)  
**Erros**: AC negativos nas histórias principais (Q5=A)  
**Prioridade**: MoSCoW (Q6=A)

---

## Resumo MoSCoW

| ID | Título | Prioridade | Personas | UC / RF |
|---|---|---|---|---|
| US-01 | Enviar lote CSV e receber confirmação assíncrona | Must | P1 | UC-01; RF-01,02,10,11,12,13 |
| US-02 | Processar e validar CSV em background | Must | P4 | UC-01 (cont.); RF-03,04,05,14,15,16; RNF-03 |
| US-03 | Consultar status e resumo de um lote | Must | P2 | UC-02; RF-06,16 |
| US-04 | Listar ingestões realizadas | Must | P2 | UC-03; RF-07 |
| US-05 | Reprocessar lote em erro | Must | P3 | UC-04; RF-08,10,15 |
| US-06 | Remover registro de ingestão | Must | P3 | UC-05; RF-09 |

*Should/Could*: nenhum neste MVP — escopo = Must acima.

---

## US-01 — Enviar lote CSV e receber confirmação assíncrona

**Como** Integrador,  
**quero** enviar um arquivo CSV de clientes via API,  
**para** obter imediatamente um identificador sem esperar a validação.

**Prioridade**: Must  
**Personas**: P1  
**Mapeamento**: UC-01 · RF-01, RF-02, RF-10, RF-11, RF-12, RF-13 · RNF-01

### Critérios de aceitação (Gherkin)

```gherkin
Given um arquivo CSV válido com cabeçalho "nome,email,cpf,telefone", separador "," e UTF-8
  And tamanho do arquivo <= 5 MB
When o Integrador envia POST /lotes com o arquivo
Then a API responde 202 Accepted em no máximo algumas centenas de milissegundos
  And o corpo contém lote_id, task_id e status "PENDENTE"
  And um registro é criado na tabela lotes com status PENDENTE
  And o arquivo é persistido no volume compartilhado
  And a tarefa allowlisted é enfileirada sem processar o CSV de forma síncrona
```

```gherkin
Given um arquivo com extensão diferente de .csv ou sem arquivo
When o Integrador envia POST /lotes
Then a API rejeita a requisição com erro 4xx e mensagem clara
  And nenhum lote é criado
```

```gherkin
Given um arquivo CSV com tamanho > 5 MB
When o Integrador envia POST /lotes
Then a API rejeita com 413 ou 400 e mensagem indicando o limite
  And nenhum lote é criado
```

### Critérios adicionais (bullets)
- [ ] Nome da tarefa validado contra `TAREFAS_SUPORTADAS` antes do enfileiramento
- [ ] Argumentos da task incluem `lote_id` e caminho do arquivo (não o conteúdo)
- [ ] Cabeçalho/encoding incorretos no upload podem ser rejeitados na API **ou** tratados no worker; se rejeitados na API, resposta 4xx documentada

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-02 — Processar e validar CSV em background

**Como** Worker/Sistema,  
**quero** consumir a tarefa, validar cada linha e gravar o resumo,  
**para** que o lote termine em `CONCLUIDO` ou `ERRO` de forma durável.

**Prioridade**: Must  
**Personas**: P4  
**Mapeamento**: RF-03, RF-04, RF-05, RF-14, RF-15, RF-16 · RNF-03, RNF-08, RNF-10

### Critérios de aceitação (Gherkin)

```gherkin
Given um lote PENDENTE com CSV acessível no volume compartilhado
When o worker consome a tarefa "ingerir_clientes"
Then o status do lote passa para PROCESSANDO
  And cada linha é classificada como válida ou inválida
  And ao final o lote fica CONCLUIDO com total_linhas, linhas_validas e linhas_invalidas
  And concluido_em é preenchido
```

```gherkin
Given uma falha transitória durante o processamento
When o worker falha na tentativa
Then a tarefa é retentada até 3 vezes com backoff 60s, 120s, 240s
  And se esgotar as tentativas o lote fica ERRO com mensagem em erro
```

```gherkin
Given uma tarefa já concluída com sucesso (mesmo celery_task_id / chave de idempotência)
When a mensagem é reentregue
Then o processamento não duplica efeitos colaterais no resumo do lote
```

### Critérios de validação (bullets)
- [ ] `nome`: obrigatório, não vazio após trim
- [ ] `email`: obrigatório, formato `usuario@dominio.tld`
- [ ] `cpf`: obrigatório, 11 dígitos + dígito verificador válido
- [ ] `telefone`: opcional; se presente, só dígitos e 10–11 dígitos
- [ ] Linha que falhar qualquer regra incrementa `linhas_invalidas` (sem correção automática)
- [ ] Status canônico sempre no MySQL (não depender do backend Celery `PENDING`)
- [ ] Candidato a propriedades PBT (design/código): validade CPF/e-mail/telefone; invariante `total = válidas + inválidas`

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-03 — Consultar status e resumo de um lote

**Como** Analista,  
**quero** consultar um lote pelo ID,  
**para** ver status e contagens de qualidade.

**Prioridade**: Must  
**Personas**: P2  
**Mapeamento**: UC-02 · RF-06, RF-16

### Critérios de aceitação (Gherkin)

```gherkin
Given um lote existente com id conhecido
When o Analista chama GET /lotes/{id}
Then a resposta 200 inclui lote_id, nome_arquivo, status
  And quando CONCLUIDO inclui total_linhas, linhas_validas, linhas_invalidas
```

```gherkin
Given um id que não existe
When o Analista chama GET /lotes/{id}
Then a API responde 404 com mensagem clara
```

### Critérios adicionais (bullets)
- [ ] Status refletido é o do MySQL (fonte da verdade)
- [ ] Em `ERRO`, campo `erro` (ou equivalente) disponível na resposta

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-04 — Listar ingestões realizadas

**Como** Analista,  
**quero** listar todas as ingestões,  
**para** ter visão do histórico de lotes.

**Prioridade**: Must  
**Personas**: P2  
**Mapeamento**: UC-03 · RF-07

### Critérios de aceitação (Gherkin)

```gherkin
Given zero ou mais lotes cadastrados
When o Analista chama GET /lotes
Then a API responde 200 com a lista de lotes (pode ser vazia)
  And cada item inclui ao menos lote_id, nome_arquivo e status
```

### Critérios adicionais (bullets)
- [ ] Sem paginação obrigatória no MVP (aceitável lista completa)
- [ ] Ordenação estável documentada (ex.: mais recente primeiro) — Should implícito se fácil

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-05 — Reprocessar lote em erro

**Como** Operador,  
**quero** reprocessar um lote que falhou,  
**para** tentar novamente a validação sem recriar o lote.

**Prioridade**: Must  
**Personas**: P3  
**Mapeamento**: UC-04 · RF-08, RF-10, RF-15

### Critérios de aceitação (Gherkin)

```gherkin
Given um lote com status ERRO e arquivo ainda presente no volume
When o Operador chama PUT /lotes/{id}
Then uma nova tarefa allowlisted é enfileirada
  And o lote volta para PENDENTE (ou PROCESSANDO conforme design)
  And a resposta indica o novo task_id
```

```gherkin
Given um lote com status PENDENTE, PROCESSANDO ou CONCLUIDO
When o Operador chama PUT /lotes/{id}
Then a API rejeita com 4xx (ex.: 409/400) e não enfileira nova tarefa
```

```gherkin
Given um id inexistente
When o Operador chama PUT /lotes/{id}
Then a API responde 404
```

### Critérios adicionais (bullets)
- [ ] Reprocessamento respeita allowlist e idempotência da nova task
- [ ] Contagens anteriores são sobrescritas ao concluir o novo processamento

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-06 — Remover registro de ingestão

**Como** Operador,  
**quero** remover o registro de uma ingestão no banco,  
**para** limpar o catálogo de lotes.

**Prioridade**: Must  
**Personas**: P3  
**Mapeamento**: UC-05 · RF-09

### Critérios de aceitação (Gherkin)

```gherkin
Given um lote existente
When o Operador chama DELETE /lotes/{id}
Then o registro é removido do MySQL
  And a API responde 204 ou 200 de sucesso
  And o arquivo CSV no volume permanece (não é apagado)
```

```gherkin
Given um id inexistente
When o Operador chama DELETE /lotes/{id}
Then a API responde 404
```

### Critérios adicionais (bullets)
- [ ] Comportamento de DELETE durante `PROCESSANDO` documentado (recomendação MVP: permitir delete do registro; worker trata lote ausente como falha sem recriar)

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## Rastreabilidade UC ↔ Histórias

| UC | História |
|---|---|
| UC-01 | US-01 + US-02 |
| UC-02 | US-03 |
| UC-03 | US-04 |
| UC-04 | US-05 |
| UC-05 | US-06 |

## Conformidade de extensões
| Extensão | Status | Nota |
|---|---|---|
| Security | Disabled | N/A |
| Resiliency | Disabled | N/A |
| PBT | Enabled | US-02 marca propriedades candidatas; detalhamento em Functional Design |
