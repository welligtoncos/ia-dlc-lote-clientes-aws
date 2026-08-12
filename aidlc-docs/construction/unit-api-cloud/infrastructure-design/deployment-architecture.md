# Arquitetura de Implantação — unit-api-cloud

```text
[Compose]
  api:8000
    STORAGE_BACKEND=fs
    STORAGE_LOCAL_DIR=/data
    volume lotes_files:/data
    -> Valkey / MySQL

[AWS dev]
  API Gateway + API Key
       |
      ALB
       |
  ECS Fargate (lote-api)
    STORAGE_BACKEND=s3
    S3_BUCKET=...
    AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY  (Q6=B; via Secrets)
    CELERY_BROKER_URL -> ElastiCache
    DATABASE_URL -> RDS
       |
       +-- PutObject S3 (libs)
       +-- enqueue Celery {lote_id, bucket, chave}
```

## Ordem

1. Code Generation desta unit (AdaptadorCelery dual kwargs + validação env s3/keys)  
2. unit-worker-s3  
3. unit-infra-aws (ECS task def com secrets/env)
