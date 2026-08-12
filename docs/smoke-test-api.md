# Smoke test — ingestão de clientes (MVP local)

Guia manual para validar API + worker com Docker Compose.

## Pré-requisitos

```bash
docker compose up -d --build
curl http://localhost:8000/health
```

Arquivo de fixture: `fixtures/clientes.csv`  
(cabeçalho `nome,email,cpf,telefone`, UTF-8, separador `,`; CPFs com 11 dígitos e DV válido)

---

## Passos executados (2026-08-12) — ciclo completo

### 1. Upload CSV → `PENDENTE`

```bash
curl -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv"
```

**Resposta observada (exemplo lote 4):**

```json
{"lote_id":4,"task_id":"b5b7cfd8-dd7c-4563-bee1-3fd8566382f9","status":"PENDENTE"}
```

### 2. Worker processa → `CONCLUIDO`

```bash
docker compose logs -f worker
```

**Logs observados (lote 5 — fila limpa):**

```text
Task ingerir_clientes[2897deac-...] received
{"mensagem":"inicio processamento","lote_id":5,"tentativa":1,...}
{"mensagem":"fim processamento","lote_id":5,"status_final":"CONCLUIDO",...}
Task ... succeeded in ~0.06s: 'CONCLUIDO'
```

### 3. Consultar lote

```bash
curl http://localhost:8000/lotes/2
```

**Resposta observada:**

```json
{
  "lote_id": 2,
  "nome_arquivo": "clientes.csv",
  "status": "CONCLUIDO",
  "total_linhas": 4,
  "linhas_validas": 4,
  "linhas_invalidas": 0,
  "criado_em": "2026-08-12T04:05:53",
  "erro": null
}
```

| Campo | Esperado / observado |
|---|---|
| `status` | `CONCLUIDO` |
| `total_linhas` | 4 (fixture) |
| `linhas_validas` | 4 |
| `linhas_invalidas` | 0 |

### 4. Listar / remover (opcional)

```bash
curl http://localhost:8000/lotes
curl -X DELETE http://localhost:8000/lotes/{id}
```

---

## Lição: task “zumbi” na fila

Se um upload foi feito **antes** do worker existir (ou o lote foi `DELETE` depois), a mensagem permanece no Valkey. Ao subir o worker aparece:

```text
ErroRetentavel('lote N nao encontrado') → RETRY 60s / 120s / 240s
```

Isso **não** invalida o teste do lote novo. Para limpar a fila:

```bash
docker compose exec valkey valkey-cli -n 0 FLUSHDB
docker compose restart worker
```

Após o flush, um novo POST (ex.: lote 5) deve aparecer sozinho nos logs, sem retries de lotes antigos.

---

## Observações

- CPF com máscara (`529.982.247-25`) conta como **inválido**; use só dígitos.
- Docs interativas: http://localhost:8000/docs
- Sem Flower/Prometheus neste ciclo.

## Testes automatizados

```bash
pip install -e ./libs -e "./api[dev]" -e "./worker[dev]"
pytest libs/tests api/tests worker/tests -v --import-mode=importlib
```
