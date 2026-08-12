# Smoke cloud (pos-deploy)

1. Obter URL: `terraform output -raw api_gateway_url`
2. Obter API key: Secrets Manager ARN em `api_key_secret_arn` (campo `api_key`)
3. Health:

```bash
curl -sS -H "x-api-key: $API_KEY" "$API_URL/health"
```

4. Upload smoke (CSV pequeno) via `POST /lotes` com multipart.
5. Verificar logs CloudWatch `/ecs/lote-dev/api` e `/ecs/lote-dev/worker`.
6. Confirmar objeto em S3 prefixo `lotes/` e status do lote em RDS.
