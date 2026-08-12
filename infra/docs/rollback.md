# Rollback (dev)

## Aplicacao (imagens)

1. Identificar tag ECR anterior estavel.
2. Atualizar `api_image` / `worker_image` (tfvars ou workflow) e `terraform apply`, **ou**
3. `aws ecs update-service --force-new-deployment` apos retag.

## Infraestrutura (Terraform)

1. Reverter o commit no git (PR).
2. GHA aplica o state desejado; ou localmente:

```bash
cd infra/terraform/envs/dev
terraform apply
```

3. Se apply destrutivo: consultar state + backups RDS antes.

Change management: mudancas TF/GHA so via PR + merge (US-AWS-07).
