# Storage Summary — unit-libs-storage

| Componente | Responsabilidade |
|---|---|
| `montar_chave` | Prefixo `lotes/` → ref relativa |
| `ArmazenamentoArquivoLocal` | fs sob `diretorio_base` |
| `ArmazenamentoArquivoS3` | boto3 upload/download_fileobj |
| `criar_armazenamento` | `fs` \| `s3` |

Porta: `salvar` / `existe` / `abrir`.
