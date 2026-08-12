# Padrões NFR — unit-infra-aws

**Decisões**: Q1–Q6 = A

---

## Resiliência (Q1=A)

| Padrão | Aplicação |
|---|---|
| Single-AZ conscious | `dev` sem Multi-AZ |
| Managed backups | RDS automated backups (default AWS retention mínima aceitável) |
| Sem failover custom | Sem read replica / scripts DR neste ciclo |

## Escalabilidade (Q2=A)

| Padrão | Aplicação |
|---|---|
| Fixed desired count | ECS api=1, worker=1 |
| Fargate capacity | Sem auto-scale policies |

## Desempenho (Q3=A)

| Padrão | Aplicação |
|---|---|
| Variables-driven sizing | `tfvars` / variables: instance classes, cpu/mem |
| Sem modos especiais | Sem PI obrigatório / provisioned throughput |

## Segurança — Defense-in-depth (Q4=A)

| Padrão | Aplicação |
|---|---|
| Tiered SGs | ALB→api; api/worker→RDS/cache/S3 |
| Edge auth | API Key só no API Gateway |
| Secrets injection | Secrets Manager → env ECS |
| Encryption at rest | S3 SSE-S3 |
| State hygiene | `sensitive` + remote state; sem secrets em git |

## Mapeamento NFR → padrão

| NFR | Padrão |
|---|---|
| NFR-INF-AVAIL-* | Single-AZ + backups |
| NFR-INF-SCALE-* | Fixed count |
| NFR-INF-PERF-* | Variables sizing |
| NFR-INF-SEC-* | Defense-in-depth |
| NFR-INF-OBS-* | CW Logs (módulo observability) |
| NFR-INF-IAC-* | TF modules + remote state + GHA |
