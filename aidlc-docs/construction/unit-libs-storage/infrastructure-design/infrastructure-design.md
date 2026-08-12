# Design de Infraestrutura — unit-libs-storage

**Decisões**: Q1=B · Q2=A · Q3=A · Q4=A · Q5=A · Q6=A · Q7=A · Q8=A · Q9=A

---

## Papel da unidade

`lote-shared` **não** é um serviço runtime. Implantação = embutida em api/worker **e** publicação em **CodeArtifact** (Q1=B) para consumo versionado, além de path/editable no monorepo local.

---

## Mapeamento lógico → infra

| Componente lógico | Infra / recurso | Onde provisiona |
|---|---|---|
| ArmazenamentoArquivoLocal | Volume Compose `/data/lotes` (`STORAGE_LOCAL_DIR`) | Compose (já existe) |
| ArmazenamentoArquivoS3 | Bucket S3 + prefixo `lotes/` | **unit-infra-aws** (Terraform) |
| criar_armazenamento | Env nos tasks ECS / Compose | Consumidores + TF |
| Pacote Python | CodeArtifact domain/repo + publish CI | Esta unit (pipeline lib) + GHA |
| IAM S3 | Task roles api/worker | unit-infra-aws (contrato abaixo) |

---

## Variáveis de ambiente (contrato Q7=A)

| Variável | Obrigatória | Default | Uso |
|---|---|---|---|
| `STORAGE_BACKEND` | não | `fs` | `fs` \| `s3` |
| `STORAGE_LOCAL_DIR` | se `fs` | `/data/lotes` | Base filesystem |
| `S3_BUCKET` | se `s3` | — | Nome do bucket |
| `AWS_REGION` | recomendado | `us-east-1` | Client boto3 |
| `S3_PREFIX` | não | `lotes/` | Prefixo de chave |

Credenciais S3: **não** via env de access key na app — task role / instance profile / local AWS profile.

---

## IAM lógico (Q8=A) — implementação TF depois

Nas task roles de api e worker (quando `STORAGE_BACKEND=s3`):

```text
s3:PutObject  on arn:aws:s3:::<bucket>/lotes/*
s3:GetObject  on arn:aws:s3:::<bucket>/lotes/*
s3:HeadObject / ListBucket (se necessário para head) no bucket com prefix condition
```

Sem `s3:*` no bucket inteiro sem prefixo.

---

## CodeArtifact (Q1=B)

| Item | Decisão |
|---|---|
| Objetivo | Publicar `lote-shared` versionado para builds ECS/CI |
| Dev local | Continua path/editable (`pip install -e libs`) |
| CI desta unit | Job de publish (versão a partir de `pyproject.toml` / tag) |
| Consumo | api/worker em CI podem instalar do CodeArtifact **ou** wheel do artifact da mesma pipeline |

Detalhe de domínio/repo AWS names → unit-infra-aws + workflow GHA.

---

## Explicitamente fora

| Item | Unit |
|---|---|
| Criação do bucket, encryption, block public access | unit-infra-aws |
| VPC endpoint S3 | unit-infra-aws (Q5=A — não exigido no contrato desta unit) |
| ElastiCache / RDS / API Gateway | unit-infra-aws |
| Monitoramento CloudWatch | consumidores ECS (Q6=A) |
