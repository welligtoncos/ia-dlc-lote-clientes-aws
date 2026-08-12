# Instruções de Testes End-to-End

## Propósito
Fluxo completo do operador: upload → fila → validação → consulta de resumo.

## Cenário E2E-01 — Ingestão feliz

1. Subir stack: `docker compose up -d --build`
2. Health: `curl http://localhost:8000/health`
3. Upload: `curl -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv"`
4. Acompanhar worker: `docker compose logs -f worker`
5. Consultar: `curl http://localhost:8000/lotes/{id}` → `CONCLUIDO`, contagens

**Evidência 2026-08-12**: lote 2 com `total_linhas=4`, `linhas_validas=4`, `linhas_invalidas=0`; lote 5 limpo após `FLUSHDB`.

Documento operacional: [`docs/smoke-test-api.md`](../../../docs/smoke-test-api.md)

## Cenário E2E-02 — OpenAPI

- Abrir http://localhost:8000/docs e exercer POST/GET manualmente (opcional)

## Fora de escopo E2E neste ciclo
- UI browser automatizado (Playwright/Cypress)
- Ambiente AWS
