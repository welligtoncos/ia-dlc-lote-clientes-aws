# Modelo de Lógica de Negócio — unit-infra-aws

**Decisões**: Q1–Q7 = A

---

## Capacidades (plataforma)

| Capacidade | História | Descrição |
|---|---|---|
| Provisionar stack `dev` | US-AWS-05 | Terraform single-AZ `us-east-1` completo |
| Edge autenticado | US-AWS-01 | API Gateway + API Key (`x-api-key`) → ALB → ECS api |
| Deploy contínuo `dev` | US-AWS-05 | GHA build/push ECR + `terraform apply` pós-merge |
| Runbooks dados | US-AWS-06 | Dump/restore RDS (mysqldump) documentado |
| Change / rollback | US-AWS-07 | PR obrigatório; nota rollback TF/ECR |
| Security baseline | US-AWS-08 | Privado S3/RDS/cache; least-privilege; TLS edge |

---

## Fluxo operacional

```text
PR (TF / GHA / docs)
  |
  v
merge main
  |
  v
GHA: build imagens api/worker -> push ECR
  |
  v
GHA: terraform apply (env dev)
  |
  v
Smoke checklist (runbook)
  |
  +-- OK: stack pronta (Gateway URL + API Key via Secrets)
  +-- Falha: rollback note (TF previous / tag ECR anterior)
```

## Fluxo de acesso cliente (US-AWS-01)

```text
Client + header x-api-key
  -> API Gateway (HTTPS/TLS)
  -> ALB (privado)
  -> ECS api
  -> (app: storage S3 + Celery -> ElastiCache)
Worker ECS (privado) consome fila / lê S3 / escreve RDS
```

## Layout Terraform (Q2=A)

```text
infra/terraform/
  modules/   (vpc, rds, s3, elasticache, ecr, ecs, alb, gateway, iam, secrets, ...)
  envs/dev/  (root: backend, providers, module wiring)
```
