terraform {
  required_version = ">= 1.5.0"

  # Descomente apos criar bucket/tabela de state (ver infra/docs/bootstrap-state.md)
  # backend "s3" {
  #   bucket         = "lote-tfstate-dev"
  #   key            = "envs/dev/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "lote-tf-locks"
  #   encrypt        = true
  # }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project = "lote-clientes"
      Env     = "dev"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "name_prefix" {
  type    = string
  default = "lote-dev"
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "api_image" {
  type    = string
  default = ""
}

variable "worker_image" {
  type    = string
  default = ""
}

variable "aws_access_key_id" {
  type      = string
  default   = ""
  sensitive = true
}

variable "aws_secret_access_key" {
  type      = string
  default   = ""
  sensitive = true
}

locals {
  tags = {
    Project = "lote-clientes"
    Env     = "dev"
  }
}

module "network" {
  source      = "../../modules/network"
  name_prefix = var.name_prefix
  azs         = var.azs
  tags        = local.tags
}

module "storage" {
  source      = "../../modules/storage"
  name_prefix = var.name_prefix
  tags        = local.tags
}

module "data" {
  source      = "../../modules/data"
  name_prefix = var.name_prefix
  subnet_ids  = module.network.private_data_subnet_ids
  sg_data_id  = module.network.sg_data_id
  db_password = var.db_password
  tags        = local.tags
}

module "security" {
  source      = "../../modules/security"
  name_prefix = var.name_prefix
  bucket_arn  = module.storage.bucket_arn
  tags        = local.tags
}

module "observability" {
  source      = "../../modules/observability"
  name_prefix = var.name_prefix
  tags        = local.tags
}

locals {
  app_env = {
    DATABASE_URL          = module.data.database_url
    CELERY_BROKER_URL     = module.data.celery_broker_url
    CACHE_URL             = module.data.cache_url
    STORAGE_BACKEND       = "s3"
    S3_BUCKET             = module.storage.bucket_name
    S3_PREFIX             = "lotes/"
    AWS_REGION            = var.aws_region
    AWS_ACCESS_KEY_ID     = var.aws_access_key_id
    AWS_SECRET_ACCESS_KEY = var.aws_secret_access_key
    LOG_LEVEL             = "INFO"
  }
}

module "compute" {
  source                 = "../../modules/compute"
  name_prefix            = var.name_prefix
  vpc_id                 = module.network.vpc_id
  private_app_subnet_ids = module.network.private_app_subnet_ids
  public_subnet_ids      = module.network.public_subnet_ids
  sg_alb_id              = module.network.sg_alb_id
  sg_ecs_id              = module.network.sg_ecs_id
  ecs_execution_role_arn = module.security.ecs_execution_role_arn
  api_task_role_arn      = module.security.api_task_role_arn
  worker_task_role_arn   = module.security.worker_task_role_arn
  api_image              = var.api_image
  worker_image           = var.worker_image
  api_log_group_name     = module.observability.api_log_group_name
  worker_log_group_name  = module.observability.worker_log_group_name
  aws_region             = var.aws_region
  environment            = local.app_env
  tags                   = local.tags
}

module "edge" {
  source                 = "../../modules/edge"
  name_prefix            = var.name_prefix
  private_app_subnet_ids = module.network.private_app_subnet_ids
  sg_vpclink_id          = module.network.sg_alb_id
  alb_listener_arn       = module.compute.alb_listener_arn
  tags                   = local.tags
}

output "api_gateway_url" {
  value = module.edge.api_endpoint
}

output "api_key_secret_arn" {
  value = module.edge.api_key_secret_arn
}

output "s3_bucket" {
  value = module.storage.bucket_name
}

output "rds_endpoint" {
  value = module.data.rds_endpoint
}

output "redis_endpoint" {
  value = module.data.redis_endpoint
}

output "ecr_api_url" {
  value = module.compute.ecr_api_url
}

output "ecr_worker_url" {
  value = module.compute.ecr_worker_url
}

output "ecs_cluster_name" {
  value = module.compute.ecs_cluster_name
}
