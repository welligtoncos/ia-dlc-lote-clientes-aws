# Dependências entre Unidades — Fase 2 AWS

## Matriz

| Unidade | Depende de | Dependentes | Tipo |
|---|---|---|---|
| `unit-libs-storage` | — | api-cloud, worker-s3 | build-time (pacote) |
| `unit-api-cloud` | libs-storage | infra (imagem api) | build + runtime contrato task |
| `unit-worker-s3` | libs-storage | infra (imagem worker) | build + runtime kwargs |
| `unit-infra-aws` | imagens api/worker publicáveis | — | deploy; provisiona RDS/S3/ECS/Gateway |

## Grafo

```text
unit-libs-storage
       |
       +----------+
       v          v
unit-api-cloud  unit-worker-s3
       |          |
       +----+-----+
            v
     unit-infra-aws
     (ECR, ECS, TF, GHA)
```

## Coordenação

| Ponto | Acordo |
|---|---|
| Contrato storage | Porta + ref opaca (App Design Q2=A) |
| Kwargs task | fs: `{lote_id, caminho}` · s3: `{lote_id, bucket, chave}` |
| Env | `STORAGE_BACKEND`, bucket, region, `DATABASE_URL`, broker |
| Ordem merge | libs → api → worker → infra (Q6=A) |
| Checkpoint testes | testes lib; Compose smoke após api+worker; terraform plan; smoke cloud pós-apply |

## Rollback

- App: redeploy tag ECR anterior (nota em runbook — US-AWS-07)
- Infra: `terraform apply` de revisão anterior / destroy seletivo em `dev`
