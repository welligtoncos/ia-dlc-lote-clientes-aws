# Modelo de Lógica de Negócio — unit-api-cloud

**Decisões**: Q1–Q7 = A  
**Escopo**: tradução de kwargs Celery no AdaptadorCelery; casos de uso agnósticos ao backend

---

## Capacidades

| Capacidade | Descrição |
|---|---|
| Ingerir / reprocessar | Inalterados na Application: salvam ref, passam `{lote_id, ref}` à porta de tarefa |
| Traduzir enqueue | AdaptadorCelery monta kwargs fs ou s3 |
| HTTP | Contrato `/lotes` + `/health` sem API Key na app |

---

## Fluxo — enqueue (novo)

```text
CasoUsoIngerir / Reprocessar
  payload_minimo = { lote_id, ref }   # ref = lote.caminho_arquivo
        |
        v
AdaptadorCelery.executar(nome, payload_minimo)
        |
        +-- STORAGE_BACKEND=fs
        |     kwargs = { lote_id, caminho: ref }
        |
        +-- STORAGE_BACKEND=s3
              kwargs = { lote_id, bucket: cfg.s3_bucket, chave: ref }
        |
        v
Celery send_task("ingerir_clientes", kwargs=...)
```

## Fluxo — HTTP (inalterado)

```text
Client (+ API Key no Gateway, fora da app)
  -> POST /lotes -> 202 { lote_id, task_id, status }
  -> GET/PUT/DELETE /lotes...
  -> GET /health
```

---

## Limites

- Sem validação de API Key na FastAPI (Q5=A)
- Sem Terraform / Gateway (unit-infra-aws)
- Worker dual kwargs → unit-worker-s3 (api já envia formato cloud)
