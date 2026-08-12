# Arquitetura de Implantação — unit-libs-storage

## Visão

```text
[Dev monorepo]
  pip install -e libs/  ----------------------> api / worker locais
        |
        v
[CI - unit-libs-storage]
  pytest + moto
  twine/poetry publish --> CodeArtifact (lote-shared)
        |
        v
[CI - api/worker images]
  pip install lote-shared==x.y.z  (CodeArtifact)
  ou COPY wheel da mesma pipeline
        |
        v
[ECS Fargate api/worker]  STORAGE_BACKEND=s3
        |
        +--> S3 bucket/lotes/*   (IAM task role)
[Compose] STORAGE_BACKEND=fs
        |
        +--> volume /data/lotes
```

## Ambientes

| Ambiente | Storage | Como obtém a lib |
|---|---|---|
| Local Compose | `fs` + volume | editable path |
| CI testes lib | moto / tmp fs | checkout |
| AWS `dev` | `s3` | imagem com pacote CodeArtifact ou wheel |

## Compute / rede / messaging

N/A na lib (Q2/Q4/Q5=A). Serviços runtime = api/worker.

## Dependência de ordem

1. Code desta unit (lib + testes + publish workflow esqueleto)  
2. unit-api-cloud / unit-worker-s3 consomem nova API da porta  
3. unit-infra-aws cria bucket + IAM alinhados a este contrato  
4. GHA apply sobe ECS com env S3
