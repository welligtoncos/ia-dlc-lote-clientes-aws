# lote-shared

Dominio, portas, persistence, validacao e **storage** (fs/S3) compartilhados.

## Storage (Fase 2)

```python
from lote_shared.storage import criar_armazenamento

store = criar_armazenamento(
    "fs",  # ou "s3"
    diretorio_base="/data",
    # bucket="meu-bucket", region="us-east-1",
)
ref = store.salvar("1_clientes.csv", b"...")  # -> "lotes/1_clientes.csv"
store.abrir(ref)
```

### Env

| Var | Default | Uso |
|---|---|---|
| `STORAGE_BACKEND` | `fs` | `fs` \| `s3` |
| `STORAGE_LOCAL_DIR` | — | Base fs (Compose: `/data`) |
| `S3_BUCKET` | — | Obrigatorio se s3 |
| `AWS_REGION` | `us-east-1` | |
| `S3_PREFIX` | `lotes/` | |

Credenciais S3: default credential chain (task role / profile). Sem keys no codigo.

## Dev

```bash
cd libs
pip install -e ".[dev]"
pytest -q
```

## CodeArtifact

Workflow esqueleto: `.github/workflows/publish-lote-shared.yml`.  
Local continua com `pip install -e libs`. Publique tags `lote-shared-v*` apos configurar dominio/repo AWS.
