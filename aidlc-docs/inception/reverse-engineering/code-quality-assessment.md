# Avaliação de Qualidade de Código

## Cobertura de Testes
- **Geral**: Boa para MVP (30 testes unitários + smoke E2E manual)
- **Testes Unitários**: Presentes (api, worker, libs + PBT)
- **Testes de Integração**: Manuais via compose (documentados); sem suite pytest Docker

## Indicadores
- **Linting**: Não configurado formalmente (sem ruff/flake8 no repo)
- **Estilo**: Consistente (PT, hexagonal)
- **Documentação**: Boa (aidlc-docs + docs/fluxo + smoke)

## Débito Técnico / gaps migração
- Storage apenas filesystem (bloqueia S3 sem adapter)
- `datetime.utcnow()` deprecated (warnings)
- Sem Terraform / IAM versionado como código (script IAM interrompido/parcial no disco)
- Sem auth na API (aceitável MVP; Gateway pode adicionar depois)
- Sem CI/CD GitHub Actions ainda

## Padrões
- **Bons**: isolamento de projetos, allowlist de task, enqueue degradado, idempotência worker, PBT
- **Atenção**: tasks zumbis no broker se lote deletado; payload path acoplado ao volume
