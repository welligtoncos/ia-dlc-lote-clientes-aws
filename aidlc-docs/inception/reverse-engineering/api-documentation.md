# Documentação de API (as-is)

**Base URL local**: `http://localhost:8000`  
**OpenAPI**: `/docs`

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| GET | `/health` | Health check | Não |
| POST | `/lotes` | Upload CSV (`multipart` campo `arquivo`) → 202 | Não |
| GET | `/lotes` | Lista lotes (criado_em DESC) | Não |
| GET | `/lotes/{id}` | Detalhe + resumo (cache-aside) | Não |
| PUT | `/lotes/{id}` | Reprocessar se `ERRO` | Não |
| DELETE | `/lotes/{id}` | Remove registro MySQL | Não |

## POST /lotes — resposta 202

```json
{"lote_id": 1, "task_id": "<uuid>", "status": "PENDENTE"}
```

## GET /lotes/{id} — exemplo CONCLUIDO

```json
{
  "lote_id": 2,
  "nome_arquivo": "clientes.csv",
  "status": "CONCLUIDO",
  "total_linhas": 4,
  "linhas_validas": 4,
  "linhas_invalidas": 0,
  "criado_em": "...",
  "erro": null
}
```

## Contrato de fila (não HTTP)

- Task: `ingerir_clientes`
- Kwargs: `{lote_id: int, caminho: str}`

## Implicação AWS

API Gateway deve fazer proxy das mesmas rotas; validar limite de payload ≥ 5 MB.
