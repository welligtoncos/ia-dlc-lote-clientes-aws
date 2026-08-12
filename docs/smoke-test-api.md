# Smoke test — unit-dominio-api (MVP local)

Guia manual para validar a API com Docker Compose **antes** do worker existir.

## Pré-requisitos

```bash
docker compose up -d --build mysql valkey api
curl http://localhost:8000/health
```

Arquivo de fixture: `fixtures/clientes.csv`  
(cabeçalho `nome,email,cpf,telefone`, UTF-8, separador `,`)

## Passos executados (2026-08-12)

### 1. Upload CSV → `202` / corpo com lote PENDENTE

```bash
curl -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv"
```

**Resposta observada:**

```json
{"lote_id":1,"task_id":"671e84d7-64fc-445c-bd44-9fbc9464d694","status":"PENDENTE"}
```

| Campo | Esperado |
|---|---|
| `lote_id` | ID numérico do lote |
| `task_id` | UUID da task Celery (enqueue no Valkey OK) |
| `status` | `PENDENTE` |

### 2. Listar lotes

```bash
curl http://localhost:8000/lotes
```

**Resposta observada:**

```json
[{"lote_id":1,"nome_arquivo":"clientes.csv","status":"PENDENTE","total_linhas":0,"linhas_validas":0,"linhas_invalidas":0,"criado_em":"2026-08-12T03:42:09","erro":null}]
```

Contagens em `0` são esperadas: o worker ainda não processa o CSV.

### 3. Consultar por ID

```bash
curl http://localhost:8000/lotes/1
```

**Resposta observada:** mesmo payload do item na lista (status `PENDENTE`).

### 4. Remover registro (arquivo permanece no volume)

```bash
curl -X DELETE http://localhost:8000/lotes/1
```

Após o delete, `GET /lotes/1` deve retornar `404`.

## Limitações deste ciclo

- Não há consumidor Celery (`unit-worker-validacao` ainda não implementada).
- Status **não** avança para `PROCESSADO` / `ERRO`.
- `PUT` reprocessar só se aplica a lotes em `ERRO` — não testável até o worker existir.
- Docs interativas: http://localhost:8000/docs

## Testes automatizados (complementar)

```bash
pip install -e ./libs -e "./api[dev]"
pytest libs/tests api/tests -v
```
