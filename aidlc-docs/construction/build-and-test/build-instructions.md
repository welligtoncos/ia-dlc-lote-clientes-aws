# Instruções de Build

## Pré-requisitos
- **Ferramenta de Build**: Docker Compose v2 + Python **3.12+** (pip/setuptools)
- **Dependências**: Docker Engine; opcionalmente venv local para testes sem container
- **Variáveis de Ambiente**: ver `.env.example` (`DATABASE_URL`, `CELERY_BROKER_URL`, `CACHE_URL`, `STORAGE_PATH`, `LOG_LEVEL`)
- **Requisitos de Sistema**: Windows/Linux/macOS com Docker; ~2 GB RAM livre; portas **8000**, **3306**, **6379**

## Projetos

| Pasta | Pacote | Artefato |
|---|---|---|
| `libs/` | `lote-shared` | biblioteca instalável |
| `api/` | `lote-api` | imagem `api` + pacote |
| `worker/` | `lote-worker` | imagem `worker` + pacote |

## Etapas de Build

### 1. Instalar Dependências (dev local)

```bash
cd c:\welligton-aws\ia-dlc-lote-clientes-aws
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -e ./libs -e "./api[dev]" -e "./worker[dev]"
```

### 2. Configurar Ambiente

```bash
copy .env.example .env
# Ajuste se MySQL/Valkey não estiverem nos defaults do compose
```

### 3. Compilar / construir imagens (todas as unidades)

```bash
docker compose build
# ou stack completa:
docker compose up -d --build
```

### 4. Verificar Sucesso do Build
- **Saída Esperada**: serviços `mysql`, `valkey`, `api`, `worker` healthy/up; `curl http://localhost:8000/health` → 200
- **Artefatos de Build**: imagens Docker locais `api`, `worker`; pacotes editable em `.venv`
- **Avisos Comuns**: warnings `datetime.utcnow()` deprecado (não bloqueante)

## Solução de Problemas

### Build Falha com Erros de Dependência
- **Causa**: path `lote-shared` não instalado; Python &lt; 3.12
- **Solução**: `pip install -e ./libs` antes de api/worker; usar Python 3.12+

### Build Falha no Docker
- **Causa**: contexto de build incorreto; porta em uso
- **Solução**: build a partir da **raiz** do monorepo (`dockerfile: api/Dockerfile` / `worker/Dockerfile`); liberar 8000/3306/6379

### MySQL não fica healthy
- **Causa**: volume antigo incompatível / init SQL
- **Solução**: `docker compose down -v` (apaga dados) e `up -d --build` novamente
