# Bootstrap do remote state (executar uma vez na conta AWS)

1. Criar bucket S3 `lote-tfstate-dev` (versioning + SSE).
2. Criar tabela DynamoDB `lote-tf-locks` (PK `LockID` String) **ou** usar S3 native lock.
3. Descomentar bloco `backend "s3"` em `envs/dev/main.tf`.
4. `terraform init -migrate-state` em `infra/terraform/envs/dev`.

OIDC (GHA): criar IAM role confiando no GitHub OIDC provider do repo; secret `AWS_ROLE_ARN`.
