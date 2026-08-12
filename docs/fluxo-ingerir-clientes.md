# Fluxo de execução — task `ingerir_clientes`

Diagrama do ciclo assíncrono no MVP local (API → Valkey → Worker → MySQL).

## Sequência

```mermaid
sequenceDiagram
    participant C as Cliente
    participant API as lote-api
    participant FS as Volume lotes_files
    participant DB as MySQL
    participant V as Valkey DB0
    participant W as lote-worker
    participant Cache as Valkey DB1

    C->>API: POST /lotes (CSV)
    API->>DB: INSERT lote PENDENTE
    API->>FS: salva {lote_id}_arquivo.csv
    API->>V: send_task("ingerir_clientes", {lote_id, caminho})
    API-->>C: 202 {lote_id, task_id, PENDENTE}

    V->>W: entrega task
    W->>DB: GET lote

    alt ja CONCLUIDO + mesmo task_id
        W-->>V: NOOP (idempotente)
    else processar
        W->>FS: le CSV (BOM, header, linhas)
        alt cabecalho invalido / arquivo ausente
            W-->>V: retry 60s, 120s, 240s
            Note over W,DB: apos 3 falhas marcar ERRO
        else header OK
            W->>DB: status PROCESSANDO
            W->>W: validar linhas (lote-shared)
            W->>DB: CONCLUIDO + contagens
            W->>Cache: DEL lote id e lista
        end
    end

    C->>API: GET /lotes/id
    API->>Cache: tenta cache
    alt miss
        API->>DB: le lote
        API->>Cache: SET
    end
    API-->>C: status + resumo
```

### Alternativa em texto (sequência)

1. Cliente faz `POST /lotes` com CSV.
2. API grava lote `PENDENTE` no MySQL e o arquivo no volume `lotes_files`.
3. API enfileira `ingerir_clientes` no Valkey DB0 com `{lote_id, caminho}` e responde `202`.
4. Worker consome a task; se já `CONCLUIDO` com o mesmo `task_id`, faz NOOP.
5. Caso contrário lê o CSV; header inválido → retry 60/120/240s → `ERRO`.
6. Header OK → `PROCESSANDO` → valida linhas → `CONCLUIDO` + contagens → invalida cache Valkey DB1.
7. Cliente consulta `GET /lotes/{id}` (cache-aside).

## Visão em camadas

```text
Cliente
   |  POST /lotes
   v
+-------------+   enqueue    +----------+
|  lote-api   |------------->| Valkey 0 |
|  FastAPI    |              |  broker  |
+------+------+              +----+-----+
       | grava CSV                | consome
       v                          v
+-------------+            +--------------+
| lotes_files |<--- le ----| lote-worker  |
+-------------+            | ingerir_...  |
                           +------+-------+
       +-------------+            |
       |   MySQL     |<-----------+ status/contagens
       +-------------+            |
       +-------------+            |
       |  Valkey 1   |<-----------+ invalidar cache
       |   cache     |
       +-------------+
```

## Código de referência

| Papel | Arquivo |
|---|---|
| Nome / allowlist API | `api/src/lote_api/application/regras_upload.py` (`TAREFA_INGERIR`) |
| Enqueue | `api/src/lote_api/infrastructure/adapters.py` (`send_task`) |
| Task worker | `worker/src/lote_worker/tasks/ingerir_clientes.py` |
| Orquestração | `worker/src/lote_worker/application/processador.py` |

## Smoke test

Ver execução prática em [`smoke-test-api.md`](smoke-test-api.md).
