# Infraestrutura Compartilhada (MVP local)

**Referenciado por**: unit-dominio-api · unit-worker-validacao  
**Orquestração**: **um** `docker-compose.yml` na **raiz** do monorepo  
**Projetos Python**: separados (`api/`, `worker/`, `libs/`)

---

## Recursos compartilhados

| Recurso | Spec | Consumidores |
|---|---|---|
| MySQL 8 | DB `lote`, user/senha via env | api, worker |
| Valkey | `:6379` — **DB 0** broker Celery; **DB 1** cache GET + invalidação | api (broker+cache), worker (broker + **invalidação cache**) |
| Volume `lotes_files` | path container `/data/lotes` | api (write), worker (read na prática; mount RW) |
| Rede Compose | bridge default / `lote-net` | todos |

---

## Contratos de conexão

| Uso | URL / path |
|---|---|
| SQLAlchemy | `mysql+pymysql://...@mysql:3306/lote` |
| Celery broker | `redis://valkey:6379/0` |
| Cache | `redis://valkey:6379/1` |
| Arquivos | `/data/lotes` (`STORAGE_PATH`) |

---

## Serviços de aplicação

| Serviço | Imagem | Portas host | Notas |
|---|---|---|---|
| `api` | `api/Dockerfile` | 8000:8000 | Uvicorn |
| `worker` | `worker/Dockerfile` | **nenhuma** | `celery ... --concurrency=2`; depends_on mysql healthy + valkey |

---

## Regras

1. Não duplicar MySQL/Valkey/volume em composes por projeto.
2. Api e worker **devem** montar o mesmo volume nomeado.
3. Worker sobe por padrão (sem profile placeholder).
4. Mudanças neste arquivo exigem alinhamento das duas unidades.
5. Esboço AWS futuro não altera estes contratos locais (só troca hosts via env).

---

## Arquivos na raiz

```text
docker-compose.yml
.env.example
infra/README.md
api/Dockerfile
worker/Dockerfile
```
