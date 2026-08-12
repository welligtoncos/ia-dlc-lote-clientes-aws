# Tech Stack Decisions — unit-api-cloud

**Decisões**: Q5=A · Q6=A

---

| Área | Decisão | Justificativa |
|---|---|---|
| HTTP | FastAPI (existente) | Sem troca de framework |
| Settings | pydantic-settings | Já usado; campos `storage_backend`, `s3_bucket` |
| Fila | Celery client via `AdaptadorCelery` | Evoluir tradução kwargs apenas |
| Storage | `lote-shared.criar_armazenamento` | unit-libs-storage |
| Auth app | Nenhuma | API Key no Gateway |
| Testes | pytest + mock Celery | NFR-API-TEST-01 |

## Explicitamente fora

| Item | Onde |
|---|---|
| API Gateway, ALB, ECS task def | unit-infra-aws |
| Consumo `{bucket,chave}` no worker | unit-worker-s3 |
