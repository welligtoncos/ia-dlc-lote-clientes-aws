# Arquitetura de Implantação — unit-worker-s3

```text
[Compose]
  worker (celery --concurrency=2)
    STORAGE_BACKEND=fs
    STORAGE_LOCAL_DIR=/data
    volume lotes_files:/data
    -> Valkey / MySQL
    task kwargs: {lote_id, caminho}

[AWS dev]
  ECS Fargate (lote-worker) — rede privada
    STORAGE_BACKEND=s3
    S3_BUCKET=...
    AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY  (Q6=A; via Secrets)
    CELERY_BROKER_URL -> ElastiCache
    DATABASE_URL -> RDS
       |
       +-- consome task {lote_id, bucket, chave}
       +-- GetObject S3 (libs.abrir)
       +-- MySQL upsert / status lote
```

## Ordem

1. Code Generation desta unit (dual kwargs + `abrir` + fail-fast keys + `.env.example`)  
2. unit-infra-aws (ECS worker task def com secrets/env)
