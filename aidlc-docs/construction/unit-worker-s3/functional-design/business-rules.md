# Regras de Negócio — unit-worker-s3

## RN-TASK — Assinatura (Q1=A)

| ID | Regra |
|---|---|
| RN-T01 | Task `ingerir_clientes(lote_id, caminho=None, bucket=None, chave=None)` |
| RN-T02 | Modo fs: `caminho` obrigatório; `bucket`/`chave` ausentes |
| RN-T03 | Modo s3: `bucket` e `chave` obrigatórios; `caminho` ausente |
| RN-T04 | Modo ambíguo ou incompleto → `ErroRetentavel` (ou erro de config na bootstrap) |

## RN-IO — Obtenção do CSV (Q2=A, Q3=A)

| ID | Regra |
|---|---|
| RN-IO01 | Bytes via `PortaArmazenamentoArquivo.abrir` (lib); sem boto3 no processador |
| RN-IO02 | fs: factory com `STORAGE_LOCAL_DIR`; ref = `caminho` |
| RN-IO03 | s3: factory com `bucket` do kwargs (ou env); ref = `chave` |
| RN-IO04 | Parse CSV a partir de bytes (`ler_csv_clientes_de_bytes` / TextIO utf-8-sig) |
| RN-IO05 | `ObjetoNaoEncontrado` / arquivo ausente → `ErroRetentavel` |

## RN-SEC — Credenciais (Q4=B)

| ID | Regra |
|---|---|
| RN-SEC01 | Se `STORAGE_BACKEND=s3` (ou modo s3 na task): exigir `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` no worker (como API) |
| RN-SEC02 | Compose `fs`: sem keys |

## RN-BIZ — Inalterado (Q5=A)

| ID | Regra |
|---|---|
| RN-B01 | Retry countdowns 60/120/240; max 3 |
| RN-B02 | Idempotência CONCLUIDO + mesmo task_id → NOOP |
| RN-B03 | Validadores `lote_shared` inalterados |
| RN-B04 | `marcar_erro` só após esgotar retries |

## Mapeamento

| US | Regras |
|---|---|
| US-AWS-03 | RN-T*, RN-IO*, RN-SEC*, RN-B* |
| US-AWS-04 | RN-T02, RN-IO02 |
