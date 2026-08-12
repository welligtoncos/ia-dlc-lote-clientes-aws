# Instruções de Testes de Integração

## Propósito
Validar interação **api → Valkey → worker → MySQL → (cache invalidate)** no compose local.

## Cenários de Teste

### Cenário 1: unit-dominio-api → unit-worker-validacao (ingestão feliz)

- **Descrição**: Upload CSV; worker consome `ingerir_clientes`; lote fica `CONCLUIDO` com contagens
- **Setup**: `docker compose up -d --build`; fixture `fixtures/clientes.csv`
- **Etapas de Teste**:
  1. `curl http://localhost:8000/health`
  2. `curl -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv"`
  3. `docker compose logs -f worker` até `status_final":"CONCLUIDO"`
  4. `curl http://localhost:8000/lotes/{id}`
- **Resultados Esperados**: `status=CONCLUIDO`, `total_linhas=4`, `linhas_validas=4`, `linhas_invalidas=0`
- **Limpeza**: opcional `DELETE /lotes/{id}`; se houver tasks zumbis: `docker compose exec valkey valkey-cli -n 0 FLUSHDB`

### Cenário 2: Contrato de fila (nome da task + payload)

- **Descrição**: API `send_task("ingerir_clientes", kwargs={lote_id, caminho})` consumida pelo worker registrado com o mesmo nome
- **Setup**: stack up
- **Etapas**: POST upload e verificar log do worker com mesmo `task_id` do JSON 202
- **Resultados Esperados**: task recebida e concluída sem `KeyError`/task não registrada

### Cenário 3: Cache-aside + invalidação

- **Descrição**: Após `CONCLUIDO`, `GET /lotes/{id}` reflete contagens (worker invalidou Valkey DB1)
- **Setup**: stack up; lote processado
- **Etapas**: GET imediato após logs CONCLUIDO
- **Resultados Esperados**: JSON com status/contagens atualizados (não PENDENTE stale)

## Configurar Ambiente

```bash
docker compose up -d --build
```

## Executar (manual — smoke documentado)

Ver guia detalhado com respostas observadas: [`docs/smoke-test-api.md`](../../../docs/smoke-test-api.md)

Não há suite pytest de integração Docker neste ciclo; a validação é **manual via compose** (já executada com sucesso em 2026-08-12).

## Limpeza

```bash
docker compose down
# reset total (apaga MySQL + volumes):
docker compose down -v
```
