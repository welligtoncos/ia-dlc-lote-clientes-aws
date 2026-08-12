# Requisitos NFR — unit-infra-aws

**Decisões**: Q1–Q3=A · Q4=A (clarification) · Q5–Q7=A

---

## Disponibilidade / resiliência

| ID | Requisito |
|---|---|
| NFR-INF-AVAIL-01 | Ambiente `dev` **single-AZ** `us-east-1`; sem Multi-AZ / DR neste ciclo |
| NFR-INF-AVAIL-02 | RTO/RPO **best-effort** (alinhado Inception Resiliency) |

## Desempenho / sizing

| ID | Requisito |
|---|---|
| NFR-INF-PERF-01 | Tamanhos mínimos `dev`: RDS `db.t4g.micro` ou `small`; ElastiCache `cache.t4g.micro`; Fargate ~0.25–0.5 vCPU |
| NFR-INF-PERF-02 | Sem SLO rígido de p95 na camada de infra neste ciclo |

## Escalabilidade

| ID | Requisito |
|---|---|
| NFR-INF-SCALE-01 | **1** task ECS api + **1** task ECS worker |
| NFR-INF-SCALE-02 | Sem autoscaling neste ciclo |

## Segurança

| ID | Requisito |
|---|---|
| NFR-INF-SEC-01 | S3 encryption SSE-S3 (ou SSE-KMS gerenciado AWS); block public access |
| NFR-INF-SEC-02 | SG least-privilege; RDS/ElastiCache privados |
| NFR-INF-SEC-03 | Sem bastion EC2 público obrigatório neste ciclo |
| NFR-INF-SEC-04 | Secrets Manager/SSM; API Key + DB + AWS keys fora do git |
| NFR-INF-SEC-05 | TLS no API Gateway; IAM least-privilege (Put/Get S3 conforme papel) |

## Observabilidade

| ID | Requisito |
|---|---|
| NFR-INF-OBS-01 | CloudWatch Logs para api/worker |
| NFR-INF-OBS-02 | Métricas ECS/ALB básicas; sem X-Ray/APM obrigatório |

## IaC / CI

| ID | Requisito |
|---|---|
| NFR-INF-IAC-01 | Terraform ≥ 1.5 + AWS provider |
| NFR-INF-IAC-02 | State remoto S3 (+ DynamoDB lock ou S3 native lock) |
| NFR-INF-IAC-03 | GHA: OIDC preferido (ou keys CI em GitHub Secrets); apply `dev` pós-merge |

## Extensões

| Extensão | Nota |
|---|---|
| Security | SEC-* baseline Q4=A / FD RN-C* |
| Resiliency | AVAIL single-AZ best-effort |
| PBT | N/A nesta unit |
