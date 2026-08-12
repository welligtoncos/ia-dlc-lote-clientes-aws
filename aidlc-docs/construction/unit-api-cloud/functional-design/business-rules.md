# Regras de Negócio — unit-api-cloud

## RN-ENQ — Enfileiramento (US-AWS-02)

| ID | Regra |
|---|---|
| RN-ENQ01 | Caso de uso passa à `PortaTarefa` apenas `{lote_id, ref}` (ref = valor de `salvar` / `caminho_arquivo`) |
| RN-ENQ02 | Tradução de kwargs ocorre **somente** no `AdaptadorCelery` (Q1=A) |
| RN-ENQ03 | Se `STORAGE_BACKEND=fs` (default): kwargs finais `{lote_id, caminho}` com `caminho=ref` (Q3=A) |
| RN-ENQ04 | Se `STORAGE_BACKEND=s3`: kwargs finais `{lote_id, bucket, chave}` com `chave=ref` e `bucket` da config (Q2=A) |
| RN-ENQ05 | Nome da task permanece `ingerir_clientes` |
| RN-ENQ06 | Allowlist de tarefas inalterada |
| RN-ENQ07 | Falha no enqueue: lote permanece `PENDENTE` (comportamento Fase 1) |

## RN-REP — Reprocessamento (Q4=A)

| ID | Regra |
|---|---|
| RN-REP01 | Mesmas regras de status `ERRO` + `existe(ref)` da Fase 1 |
| RN-REP02 | Re-enqueue usa a mesma tradução RN-ENQ* com a ref já persistida |

## RN-HTTP — Contrato API (US-AWS-01, US-AWS-04)

| ID | Regra |
|---|---|
| RN-HTTP01 | Sem autenticação/autorização na FastAPI neste ciclo |
| RN-HTTP02 | Status codes e corpos MVP preservados (202, 200, 204, 4xx) |
| RN-HTTP03 | `/health` permanece disponível (já existe; Q6=A) |
| RN-HTTP04 | Compose `fs` continua funcional (US-AWS-04) |

## RN-CFG — Configuração

| ID | Regra |
|---|---|
| RN-CFG01 | `AdaptadorCelery` recebe `storage_backend`, `s3_bucket` (e opcionalmente region — não no kwargs) |
| RN-CFG02 | Backend `s3` sem bucket configurado → erro na construção ou no enqueue (falha explícita) |

## Mapeamento histórias

| US | Regras |
|---|---|
| US-AWS-01 | RN-HTTP* |
| US-AWS-02 | RN-ENQ* |
| US-AWS-04 | RN-ENQ03, RN-HTTP04 |
