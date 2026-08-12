# Modelo de Lógica de Negócio — unit-worker-validacao

**Unidade**: unit-worker-validacao (`lote-worker` + validadores em `lote-shared`)  
**História**: US-02  
**Decisões**: Q1=A, Q2=A, Q3=A, Q4=A, Q5=A, Q6=A, Q7=B, Q8=A, Q9=A

---

## Capacidade de negócio

Consumir a tarefa `ingerir_clientes`, ler o CSV no volume compartilhado, validar cada linha de cliente conforme regras de qualidade e gravar no lote o **resumo** (`total_linhas`, `linhas_validas`, `linhas_invalidas`) com status final `CONCLUIDO` ou `ERRO` — sem HTTP e sem persistir detalhe por linha (MVP).

---

## Fluxo principal — F-W1 Processar lote (US-02)

```text
1. Receber payload {lote_id, caminho} + identidade da task (celery_task_id da mensagem)
2. Carregar Lote por lote_id
   - ausente → falha de processamento (retry / ERRO)
3. Guard de idempotência (Q5=A):
   - se status == CONCLUIDO E celery_task_id do lote == task_id da mensagem → NO-OP (sair sem reler CSV)
4. Abrir arquivo em caminho (UTF-8; aceitar BOM — Q8=A)
5. Validar cabeçalho == nome,email,cpf,telefone (após strip BOM)
   - inválido (Q3=A) → falha de tentativa (não marca PROCESSANDO — Q7=B);
     retries Celery; esgotados → marcar_erro("cabeçalho inválido" ou equivalente)
6. Cabeçalho OK → marcar_processando() (Q7=B)
7. Iterar linhas de dados:
   - linha em branco / só espaços → IGNORAR (Q2=A; fora de total_linhas)
   - demais → classificar válida ou inválida (todas as regras de campo)
   - acumular total, validas, invalidas em memória
8. Persistência atômica do sucesso (Q6=A):
   - marcar_concluido(total, validas, invalidas)
   - salvar Lote (contagens + status + concluido_em)
9. Em falha transitória no meio (I/O, DB):
   - abortar tentativa sem commit de CONCLUIDO
   - retry relê CSV do zero; contagens finais só no sucesso (Q6=A)
10. Após esgotar retries → marcar_erro(mensagem) e persistir
```

**Não faz**: endpoints HTTP; apagar CSV; normalizar/mascarar campos para persistência; gravar lista de erros por linha (Q4=A).

---

## Transformações de dados

| Entrada | Transformação | Saída |
|---|---|---|
| CSV + lote PENDENTE | parse + validação linha a linha | Lote CONCLUIDO + contagens |
| CSV cabeçalho inválido | falha de processamento | Lote ERRO (após retries) |
| Reentrega task (mesmo task_id, lote CONCLUIDO) | guard idempotente | sem mudança |
| CSV com linhas em branco | filtro | não entram nas contagens |
| Linha com CPF mascarado | validação estrita 11 dígitos (Q1=A) | conta como inválida |

---

## Validação de linha (agregação lógica `LinhaCliente`)

Uma linha de dados é **válida** se **todas** as regras abaixo passam; senão incrementa `linhas_invalidas`.

| Campo | Regra de negócio |
|---|---|
| nome | obrigatório; não vazio após trim |
| email | obrigatório; formato `usuario@dominio.tld` |
| cpf | obrigatório; **exatamente 11 caracteres numéricos** + dígito verificador válido (máscara = inválido — Q1=A) |
| telefone | opcional; se presente, apenas dígitos e comprimento 10–11 |

Sem correção automática (requirements §6).

Funções puras vivem em `lote-shared.validacao` (ownership API; exercitadas/PBT nesta unidade).

---

## Integrações de negócio (contratos)

| Porta / recurso | Uso |
|---|---|
| PortaLoteRepositorio | obter, salvar (status/contagens/erro) |
| Volume / caminho do arquivo | leitura do CSV (path no payload) |
| Fila (task `ingerir_clientes`) | entrada; retry/backoff são política de execução |

---

## Propriedades Testáveis (PBT-01) — Q9=A

| ID | Categoria | Propriedade | Componente |
|---|---|---|---|
| P-VAL-01 | Oráculo / regra | `validar_cpf(s)` verdadeiro ⇔ s tem 11 dígitos e DV correto (algoritmo oficial) | validadores |
| P-VAL-02 | Invariante | `validar_email` rejeita strings sem `@` ou domínio sem `.` | validadores |
| P-VAL-03 | Invariante | `validar_telefone("")` / `None` → válido; 10–11 dígitos → válido; demais → inválido | validadores |
| P-VAL-04 | Invariante | `validar_nome` falso para vazio/whitespace | validadores |
| P-VAL-05 | Invariante | Para qualquer conjunto de classificações de linhas (não-branco): `total = validas + invalidas` | resumir_validacao |
| P-VAL-06 | Idempotência | Processar duas vezes com mesmo `celery_task_id` em lote já `CONCLUIDO` não altera contagens/status | task ingerir |
| P-VAL-07 | Invariante | CPF com máscara (pontos/hífen) **nunca** é válido sob Q1=A | validar_cpf |

Componentes sem PBT adicional: adapters de I/O Celery/filesystem — N/A (adaptadores; propriedades no domínio/validação).
