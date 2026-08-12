# Stack Tecnológica

## Linguagens
- Python **3.12+**

## Frameworks / libs
- FastAPI + Uvicorn + Pydantic v2 — API
- Celery + redis — fila
- SQLAlchemy 2 + PyMySQL — MySQL
- Hypothesis + pytest — PBT/unit
- pydantic-settings — configuração

## Infraestrutura (as-is)
- Docker / Docker Compose
- MySQL 8
- Valkey 8
- Volume Docker `lotes_files`

## Infraestrutura (alvo Fase 2 — decisões)
- Terraform
- ECS Fargate + ECR
- RDS MySQL
- API Gateway + ALB
- S3 (arquivos)
- ElastiCache Valkey/Redis
- Secrets Manager

## Build
- pip / setuptools (`pyproject.toml` por projeto)
- Docker multi-stage simples (Dockerfile por serviço)
