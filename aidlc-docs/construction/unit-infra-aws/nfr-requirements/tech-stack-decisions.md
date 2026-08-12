# Tech Stack Decisions — unit-infra-aws

**Decisões**: Q6=A

---

| Área | Decisão | Justificativa |
|---|---|---|
| IaC | Terraform ≥ 1.5 | Padrão Inception |
| Cloud | AWS `us-east-1` | Escopo Fase 2 |
| Compute | ECS Fargate | api + worker |
| Edge | API Gateway + ALB + API Key | US-AWS-01 |
| Data | RDS MySQL + ElastiCache + S3 | Paridade Compose |
| Secrets | Secrets Manager / SSM | FD Q4=A |
| CI/CD | GitHub Actions + state remoto | US-AWS-05 |
| Auth CI | OIDC (preferido) | Evitar long-lived keys |

## Explicitamente fora deste ciclo

| Item | Motivo |
|---|---|
| Multi-AZ / DR | NFR-INF-AVAIL |
| Autoscaling ECS | NFR-INF-SCALE |
| KMS CMK + bastion | Q4=A |
| X-Ray / APM | NFR-INF-OBS |
| Dump automatizado no GHA | FD Q5=A (runbook only) |
