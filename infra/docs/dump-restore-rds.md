# Dump / restore RDS (dev)

## Dump

```bash
# A partir de host com acesso a VPC (bastion/SSM ou CI com rede)
mysqldump -h "$RDS_ENDPOINT" -u lote -p lote > lote-$(date +%Y%m%d).sql
```

Armazene o dump em S3 privado (bucket operacional) — nao commit no git.

## Restore

```bash
mysql -h "$RDS_ENDPOINT" -u lote -p lote < lote-YYYYMMDD.sql
```

RTO/RPO: best-effort (single-AZ). Preferir snapshot RDS gerenciado para pontos de recuperacao.
