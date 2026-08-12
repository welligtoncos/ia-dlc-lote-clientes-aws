# Modelo de Lógica de Negócio — unit-dominio-api

**Unidade**: unit-dominio-api (`lote-api` + ownership `lote-shared`)  
**Decisões**: Q1–Q8 = A

---

## Capacidade de negócio

Gerir o ciclo de vida do **lote de ingestão** na borda HTTP: aceitar CSV, registrar lote, enfileirar processamento, consultar, reprocessar falhas e remover registros — sem executar a validação linha a linha (worker).

---

## Fluxos principais

### F1 — Ingerir clientes (US-01)

```text
1. Receber arquivo
2. Validar entrada de negocio: arquivo presente, nome termina em .csv, tamanho <= 5 MB
3. Criar Lote (status PENDENTE, nome_arquivo original)
4. Persistir Lote (obter id)
5. Salvar arquivo no armazenamento com nome {lote_id}_{nome_original}; guardar caminho no contexto do lote/task
6. Enfileirar tarefa "ingerir_clientes" com {lote_id, caminho} via PortaTarefa (allowlist)
7. Associar celery_task_id ao Lote
8. Retornar lote_id, task_id, status PENDENTE
```

**Não faz**: ler linhas, validar cabeçalho/conteúdo CSV, marcar PROCESSANDO/CONCLUIDO.

### F2 — Obter lote (US-03)

```text
1. Buscar Lote por id
2. Se ausente -> LoteNaoEncontrado
3. Retornar dados do Lote (status + resumo se houver)
```

### F3 — Listar lotes (US-04)

```text
1. Listar todos os Lotes ordenados por criado_em DESC
2. Retornar colecao (pode ser vazia) com campos minimos
```

### F4 — Reprocessar lote (US-05)

```text
1. Buscar Lote por id (senao LoteNaoEncontrado)
2. Se nao pode_reprocessar (status != ERRO) -> ReprocessamentoNaoPermitido
3. Se arquivo nao existe no armazenamento -> ArquivoAusenteParaReprocessamento (nao enfileira)
4. Transicionar ERRO -> PENDENTE; limpar mensagem de erro (e opcionalmente zerar contagens)
5. Enfileirar nova task; atualizar celery_task_id
6. Retornar lote_id, task_id, status PENDENTE
```

### F5 — Remover lote (US-06)

```text
1. Buscar Lote (senao LoteNaoEncontrado)
2. Remover registro (incluindo se PROCESSANDO)
3. Nao apagar arquivo no volume
4. Confirmar remocao
```

---

## Transformações de dados

| Entrada | Transformação | Saída |
|---|---|---|
| Upload CSV | Metadados + path | Lote PENDENTE + mensagem de fila |
| id | Lookup | Lote ou erro |
| — | Listagem ordenada | Lista de Lote |
| id (ERRO + arquivo ok) | Reset + enqueue | Lote PENDENTE + nova task |
| id | Delete registro | Ausência do Lote |

---

## Integrações de negócio (contratos, não tech)

| Porta | Uso nesta unidade |
|---|---|
| PortaLoteRepositorio | CRUD Lote |
| PortaArmazenamentoArquivo | salvar / existe |
| PortaTarefa | executar(nome, payload) → task_id |

---

## Propriedades Testáveis (PBT-01)

| ID | Categoria | Propriedade | Onde |
|---|---|---|---|
| P-API-01 | Invariante | `pode_reprocessar()` ⇔ `status == ERRO` | Lote |
| P-API-02 | Invariante | Após `criar_pendente`, status é PENDENTE e totais são 0 | Lote |
| P-API-03 | Idempotência / regra | Reprocessar a partir de status ≠ ERRO nunca produz enqueue (falha de domínio) | ReprocessarLote |
| P-API-04 | Invariante | Nome armazenado contém `lote_id` como prefixo `{id}_` | política de nome |
| P-VAL-* | — | Validadores de linha | **Adiados** à unit-worker (Q7=A); apenas esboço em libs |

Componentes sem mais propriedades PBT nesta unidade: rotas HTTP (I/O) — N/A com justificativa de serem adaptadores.
