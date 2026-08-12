# Plano de Geração de Código — unit-libs-storage

**Unidade**: `unit-libs-storage`  
**Código**: `libs/` (workspace root) — NUNCA em `aidlc-docs/`  
**Histórias**: US-AWS-02, US-AWS-04  
**Status**: Parte 2 **EXECUTADA** — libs 25 passed · api 11 passed

---

## Etapas de execução

### Etapa 1 — Exceções e porta
- [x] Adicionar `ObjetoNaoEncontrado` e `ErroArmazenamento` em `libs/src/lote_shared/domain/excecoes.py`
- [x] Estender `PortaArmazenamentoArquivo` com `abrir(self, caminho: str) -> bytes` em `ports/portas.py`
- [x] Histórias: US-AWS-02, US-AWS-04

### Etapa 2 — Helper e adapters storage
- [x] Criar `libs/src/lote_shared/storage/__init__.py`
- [x] Criar `montar_chave` + `ArmazenamentoArquivoLocal`
- [x] Criar `ArmazenamentoArquivoS3`
- [x] Criar `criar_armazenamento(backend, **cfg)`
- [x] Histórias: US-AWS-02, US-AWS-04

### Etapa 3 — Dependências pyproject
- [x] Adicionar `boto3` em dependencies de `libs/pyproject.toml`
- [x] Adicionar `moto[s3]` em optional `dev`
- [x] Histórias: NFR stack

### Etapa 4 — Testes unitários + PBT
- [x] `libs/tests/test_armazenamento_local.py`
- [x] `libs/tests/test_armazenamento_s3.py`
- [x] `libs/tests/test_referencia_pbt.py`
- [x] `libs/tests/test_factory_armazenamento.py`
- [x] Histórias: US-AWS-02, US-AWS-04 · NFR-LIB-TEST-*

### Etapa 5 — Brownfield api: remover Local duplicado
- [x] Atualizar `api/.../adapters.py`
- [x] Atualizar composition root / settings (factory + env)
- [x] Ajustar testes api (`abrir`)
- [x] Worker `leitor_csv` resolve ref relativa + compose `/data`
- [x] Histórias: US-AWS-04

### Etapa 6 — CodeArtifact / CI esqueleto
- [x] `.github/workflows/publish-lote-shared.yml`
- [x] `libs/README.md`
- [x] Histórias: infra Q1=B

### Etapa 7 — Documentação de código (aidlc-docs)
- [x] `code-generation-summary.md`
- [x] `storage-summary.md`
- [x] `.env.example` atualizado

### Etapa 8 — Verificação local
- [x] `pytest` libs (25) + api (11)
- [x] Sem arquivos `*_modified` duplicados
