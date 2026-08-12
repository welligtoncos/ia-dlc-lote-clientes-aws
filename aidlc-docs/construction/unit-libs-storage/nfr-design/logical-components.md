# Componentes Lógicos — unit-libs-storage

**Decisão Q5=A**: três peças + helper de chave.

---

## Diagrama

```text
criar_armazenamento(backend, **cfg)
        |
        +-- "fs" --> ArmazenamentoArquivoLocal(diretorio_base, prefixo)
        +-- "s3" --> ArmazenamentoArquivoS3(bucket, region?, prefixo)
                         |
                         +-- boto3 client (credential chain)
                         +-- TransferConfig (streaming / multipart threshold)

helper: montar_chave(nome_destino) -> "lotes/" + nome_destino
Porta: salvar / existe / abrir
```

---

## 1. `criar_armazenamento`

| Aspecto | Detalhe |
|---|---|
| Entrada | `backend: str`, kwargs de config |
| Saída | Implementação de `PortaArmazenamentoArquivo` |
| Regras | `fs` default; `s3` exige bucket; outro → erro |

## 2. `ArmazenamentoArquivoLocal`

| Aspecto | Detalhe |
|---|---|
| Estado | `diretorio_base`, `prefixo` |
| `salvar` | Escreve sob `base/chave`; retorna chave relativa |
| `existe` | `Path.is_file` |
| `abrir` | `read_bytes`; ausente → `ObjetoNaoEncontrado` |

## 3. `ArmazenamentoArquivoS3`

| Aspecto | Detalhe |
|---|---|
| Estado | `bucket`, `region`, `prefixo`, client boto3 |
| `salvar` | Stream upload (`upload_fileobj` / equivalente) |
| `existe` | `head_object`; 404 → False |
| `abrir` | Download stream → `bytes`; NotFound → `ObjetoNaoEncontrado` |

## 4. Helper `montar_chave` (função)

Não é classe tipada `ReferenciaArmazenamento` (Q5≠B). Função pura: aplica prefixo `lotes/`.

---

## Integração com consumidores

| Consumidor | Uso |
|---|---|
| api composition root | `criar_armazenamento(os.getenv("STORAGE_BACKEND","fs"), ...)` |
| worker | Idem; `abrir(ref)` para CSV |
| unit-api-cloud | Remove `ArmazenamentoArquivoLocal` duplicado da api |

## Infraestrutura externa (não nesta unit)

Bucket S3, IAM task role, encryption → `unit-infra-aws` / Infrastructure Design daquela unit.
