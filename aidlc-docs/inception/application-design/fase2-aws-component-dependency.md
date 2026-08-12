# Dependências de Componentes — Fase 2 AWS

## Matriz (delta)

| De → Para | Tipo | Comunicação |
|---|---|---|
| Presentation → Application | sync in-process | chamadas de caso de uso |
| Application → PortaArmazenamento | porta | ref opaca |
| Application → PortaTarefa | porta | payload `{lote_id, ref}` |
| Application → PortaRepositorio | porta | entidade Lote |
| C5 Composition → C3a/C3b | factory | instanciação por env |
| AdaptadorCelery → Broker | async | Celery/ElastiCache ou Valkey |
| Worker task → S3 | AWS SDK | quando kwargs cloud |
| Worker task → Application validators | in-process | funções puras |
| Worker / API → RDS | SQL | DATABASE_URL |
| Client → API Gateway | HTTPS + API Key | edge (fora do processo app) |
| API Gateway → ALB → ECS api | HTTPS/HTTP interno | rede VPC |

## Diagrama de dependência (app)

```text
                    [API Gateway]*     * fora do processo
                           |
                      [Presentation]
                           |
                      [Application]
                      /    |    \
                     v     v     v
              [StoragePort] [TaskPort] [RepoPort]
                     |         |          |
            +--------+--+   [Celery]     [MySQL/RDS]
            |           |
         [Local]     [S3]*
            |
     [Composition Root] escolhe Local|S3
```

## Acoplamento

- Domain **não** depende de boto3 / FastAPI / Celery
- S3 e factory ficam em `libs` (Q1=A) — api/worker não implementam cliente S3 próprio
- Terraform/GHA **não** entram na matriz de runtime da app (Q5=A)

## Extension notes
- Security: secrets e roles são fronteira infra; app só consome env/IAM role
- Resiliency: retries Celery inalterados; single-AZ é decisão de infra
