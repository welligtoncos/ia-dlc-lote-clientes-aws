# Arquitetura de Implantação — unit-infra-aws

```text
[Client]
   | HTTPS + x-api-key
   v
API Gateway (edge)
   |
   v
ALB (private subnet)
   |
   v
ECS Fargate lote-api (private) ----+--> S3 (Put)
   |                                |
   +--> ElastiCache (broker/cache)  |
   +--> RDS MySQL                   |
                                    |
ECS Fargate lote-worker (private) --+--> S3 (Get)
   |                                |
   +--> ElastiCache / RDS ----------+

[CI]
  GitHub Actions (OIDC)
    -> ECR push
    -> terraform apply envs/dev
    -> (ops) smoke checklist
```

## Rede (1 AZ)

```text
VPC
  public:  ALB (+ NAT se egress privado precisar)
  private-app: ECS api + worker
  private-data: RDS + ElastiCache
```

## Ordem Code Generation

1. Bootstrap state backend (doc + TF mínimo se necessário)
2. Módulos TF + `envs/dev`
3. Workflows GHA
4. Runbooks + README
5. Atualizar `shared-infrastructure.md` (já no design)
