# Entidades / Conceitos — unit-infra-aws

Sem entidades de domínio de clientes. Conceitos de plataforma:

## AmbienteDev

| Atributo | Valor |
|---|---|
| Região | `us-east-1` |
| AZ | single |
| IaC | Terraform modules + `envs/dev` |

## EdgeApi

| Conceito | Detalhe |
|---|---|
| Gateway | HTTPS + API Key |
| Header | `x-api-key` |
| Upstream | ALB → ECS `lote-api` |

## SegredoAplicacao

| Tipo | Exemplos | Destino |
|---|---|---|
| DB | `DATABASE_URL` / password | Secrets → env ECS |
| AWS app keys | `AWS_ACCESS_KEY_ID` / `SECRET` | Secrets → env api+worker (contrato Q6) |
| API Key value | valor Gateway | Secrets / output sensível |

## Runbook

| Documento | Conteúdo |
|---|---|
| dump-restore | mysqldump / restore RDS |
| rollback | TF previous + tag ECR |
| smoke | checklist pós-apply |

## Artefatos esperados (code-gen)

| Path | Papel |
|---|---|
| `infra/terraform/**` | Módulos + env dev |
| `.github/workflows/*` | build/push + apply |
| `infra/` ou `docs/` runbooks | US-AWS-06/07/smoke |
