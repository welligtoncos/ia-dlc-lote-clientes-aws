# Tech Stack Decisions — unit-libs-storage

**Decisões do plano**: Q5=A · Q6=A · Q7=A · Q8=A

---

## Runtime / linguagem

| Escolha | Decisão | Justificativa |
|---|---|---|
| Linguagem | Python 3.12 (já do monorepo) | Consistência com `lote-shared` |
| Pacote | `lote-shared` em `libs/` | App Design Q1=A |

## Cliente de objetos

| Escolha | Decisão | Justificativa |
|---|---|---|
| AWS SDK | **boto3** síncrono | Alinha FastAPI sync + Celery; Q5=A |
| Async S3 | Não | Evita async cascade na API |
| Instalação | Dependência **direta** de `lote-shared` | Q7=A — sempre presente |

## Backends

| Backend | Biblioteca / API | Notas |
|---|---|---|
| `fs` | `pathlib` | Local consolidado na lib |
| `s3` | `boto3.client("s3")` | Credential chain padrão |

## Testes

| Ferramenta | Uso |
|---|---|
| pytest | Suite da lib |
| moto | Mock S3 |
| hypothesis | PBT leve (refs) — alinhado PBT ON |

## Explicitamente fora desta unit

| Item | Onde |
|---|---|
| Terraform, IAM roles, bucket encryption flags | unit-infra-aws |
| Tradução kwargs Celery | unit-api-cloud / unit-worker-s3 |
| API Gateway / TLS edge | unit-infra-aws |
