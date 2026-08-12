# Regras de Negócio — unit-worker-validacao

**Decisões**: Q1=A … Q6=A, Q7=B, Q8=A, Q9=A

---

## RN-TASK — Consumo da tarefa

| ID | Regra |
|---|---|
| RN-T01 | Nome da tarefa processada: `ingerir_clientes` |
| RN-T02 | Payload mínimo: `lote_id`, `caminho` |
| RN-T03 | Status canônico do lote vive no MySQL (não usar Celery `PENDING` como verdade) |
| RN-T04 | Retry: até 3 tentativas com backoff 60s, 120s, 240s; depois `ERRO` + mensagem |
| RN-T05 | Retry **recomeça do zero** (releitura completa do CSV); sem checkpoint por linha (Q6=A) |

## RN-IDEM — Idempotência (RF-15)

| ID | Regra |
|---|---|
| RN-I01 | Se `status == CONCLUIDO` **e** `lote.celery_task_id == task_id` da mensagem → **no-op** (Q5=A) |
| RN-I02 | Reprocessamento via API (US-05) gera **novo** `celery_task_id` e status `PENDENTE` — não cai no no-op |
| RN-I03 | Lote `CONCLUIDO` com task_id **diferente** não é no-op automático desta regra (cenário excepcional; tratar como reprocessamento explícito só via fluxo API) |

## RN-CSV — Arquivo e cabeçalho

| ID | Regra |
|---|---|
| RN-C01 | Encoding UTF-8; separador `,` |
| RN-C02 | Cabeçalho obrigatório exato: `nome,email,cpf,telefone` (após trim de espaços nas células do header) |
| RN-C03 | BOM UTF-8 permitido; deve ser removido antes de comparar o header (Q8=A) |
| RN-C04 | Cabeçalho inválido/ausente → falha de tentativa; **não** marca `PROCESSANDO`; após retries → `ERRO` sem resumo de linhas (Q3=A, Q7=B) |
| RN-C05 | Arquivo ausente / ilegível → falha de tentativa → retries → `ERRO` |

## RN-STATUS — Ciclo no worker

| ID | Regra |
|---|---|
| RN-S01 | `PROCESSANDO` somente **após** cabeçalho válido (Q7=B) |
| RN-S02 | Sucesso → `CONCLUIDO` + contagens + `concluido_em`; `erro` limpo |
| RN-S03 | Falha definitiva → `ERRO` + mensagem em `erro` + `concluido_em` |
| RN-S04 | Durante retries por cabeçalho inválido, lote pode permanecer `PENDENTE` até `ERRO` |

## RN-LINHA — Classificação

| ID | Regra |
|---|---|
| RN-L01 | Linha em branco / só espaços → **ignorada** (não entra em `total_linhas`) (Q2=A) |
| RN-L02 | Demais linhas de dados incrementam `total_linhas` |
| RN-L03 | Linha válida se nome∧email∧cpf∧telefone (opcional) passam; senão `linhas_invalidas++` |
| RN-L04 | Sem persistência de motivo/número da linha inválida (Q4=A) |
| RN-L05 | Invariante ao concluir: `total_linhas == linhas_validas + linhas_invalidas` |

## RN-CAMPO — Validadores (`lote-shared`)

| ID | Campo | Regra |
|---|---|---|
| RN-F01 | nome | obrigatório; não vazio após trim |
| RN-F02 | email | obrigatório; `usuario@dominio.tld` |
| RN-F03 | cpf | exatamente **11 caracteres**, todos dígitos, + DV válido; máscara (`529.982.247-25`) = **inválido** (Q1=A) |
| RN-F04 | telefone | vazio/ausente = OK; senão só dígitos e 10–11 de comprimento |

## RN-RESUMO — Persistência do resultado

| ID | Regra |
|---|---|
| RN-R01 | Contagens finais gravadas apenas em transição para `CONCLUIDO` bem-sucedida |
| RN-R02 | Tentativas falhas não devem deixar contagens parciais “congeladas” como resultado oficial |
| RN-R03 | Worker **não** invalida cache HTTP explicitamente neste design funcional (preocupação NFR/infra da API); fonte da verdade = MySQL |

## Mapeamento

| US / RF | Regras |
|---|---|
| US-02 / RF-03,04,05,14,15,16 | RN-T*, RN-I*, RN-C*, RN-S*, RN-L*, RN-F*, RN-R* |
| RNF-03 | RN-T04, RN-T05 |
| RNF-10 (PBT) | P-VAL-* em business-logic-model.md |
