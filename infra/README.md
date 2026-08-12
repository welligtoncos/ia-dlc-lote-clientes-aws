# Esboco AWS (NAO aplicar neste ciclo)

## Mapeamento futuro
| Local | AWS |
|---|---|
| api container | ECS Fargate |
| api image | ECR |
| mysql | RDS MySQL |
| valkey | ElastiCache Valkey |
| lotes_files | EFS (ou S3 na evolucao) |
| :8000 | ALB; API Gateway opcional |

## Proximos passos (Fase 2)
1. Criar modulo Terraform ou app AWS Copilot.
2. Injetar secrets via Secrets Manager.
3. Task roles IAM para ECR/logs/secrets.

Nenhuma infra AWS e provisionada pelo MVP local.
