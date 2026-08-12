# Evolução AWS (Fase 2) — esboço

**Status**: decisões de produto sinalizadas; IaC ainda não aplicada  
**Inception AI-DLC**: em andamento (Reverse Engineering concluída — aguardando aprovação)

## Decisões sinalizadas
| Tema | Escolha |
|---|---|
| IaC | Terraform |
| Banco | RDS MySQL |
| Borda HTTP | API Gateway → ALB → ECS API |
| Arquivos | S3 |
| Compute | ECS Fargate (api + worker) + ECR |
| Fila/cache | ElastiCache Valkey/Redis |

Detalhamento as-is do sistema: `aidlc-docs/inception/reverse-engineering/`.

Nenhuma infra AWS provisionada ainda.
