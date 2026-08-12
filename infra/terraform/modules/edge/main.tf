terraform {
  required_version = ">= 1.5.0"
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

variable "name_prefix" {
  type = string
}

variable "private_app_subnet_ids" {
  type = list(string)
}

variable "sg_vpclink_id" {
  type = string
}

variable "alb_listener_arn" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

resource "random_password" "api_key" {
  length  = 32
  special = false
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${var.name_prefix}-http"
  protocol_type = "HTTP"
  tags          = var.tags
}

resource "aws_apigatewayv2_vpc_link" "this" {
  name               = "${var.name_prefix}-vpclink"
  security_group_ids = [var.sg_vpclink_id]
  subnet_ids         = var.private_app_subnet_ids
  tags               = var.tags
}

resource "aws_apigatewayv2_integration" "alb" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "HTTP_PROXY"
  integration_uri        = var.alb_listener_arn
  integration_method     = "ANY"
  connection_type        = "VPC_LINK"
  connection_id          = aws_apigatewayv2_vpc_link.this.id
  payload_format_version = "1.0"
}

resource "aws_apigatewayv2_route" "default" {
  api_id             = aws_apigatewayv2_api.http.id
  route_key          = "ANY /{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.alb.id}"
  authorization_type = "NONE"
}

resource "aws_apigatewayv2_route" "root" {
  api_id             = aws_apigatewayv2_api.http.id
  route_key          = "ANY /"
  target             = "integrations/${aws_apigatewayv2_integration.alb.id}"
  authorization_type = "NONE"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "$default"
  auto_deploy = true
  tags        = var.tags
}

resource "aws_secretsmanager_secret" "api_key" {
  name_prefix = "${var.name_prefix}-apikey-"
  description = "Client x-api-key value (HTTP API). Enforce via authorizer/WAF follow-up se necessario."
  tags        = var.tags
}

resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id = aws_secretsmanager_secret.api_key.id
  secret_string = jsonencode({
    header   = "x-api-key"
    api_key  = random_password.api_key.result
    endpoint = aws_apigatewayv2_api.http.api_endpoint
  })
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http.api_endpoint
}

output "api_key_secret_arn" {
  value = aws_secretsmanager_secret.api_key.arn
}

output "api_key_value" {
  value     = random_password.api_key.result
  sensitive = true
}
