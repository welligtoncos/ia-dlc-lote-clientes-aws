# Tech Stack Decisions — unit-worker-s3

**Decisões**: Q5=A

---

| Área | Decisão | Justificativa |
|---|---|---|
| Runtime | Celery worker (existente) | Consumidor da fila Valkey/ElastiCache |
| Task | `ingerir_clientes` com kwargs dual | Alinhado à API AdaptadorCelery |
| Storage | `lote_shared.criar_armazenamento` + `abrir` | Sem boto3 no processador |
| CSV | Parse a partir de bytes (`TextIO` / helper) | Unifica fs e s3 |
| Credenciais | Env keys se s3 | Paridade com unit-api-cloud Q6=B |
| Testes | pytest + memória/moto | NFR-WRK-TEST-01 |

## Explicitamente fora

| Item | Onde |
|---|---|
| ECS task def, Secrets, ElastiCache | unit-infra-aws |
| Tradução kwargs na API | unit-api-cloud (já feito) |
| Implementação S3 na lib | unit-libs-storage (já feito) |
