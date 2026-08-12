# Infraestrutura Compartilhada (MVP local)

**Referenciado por**: unit-dominio-api · unit-worker-validacao  
**Orquestração**: **um** `docker-compose.yml` na **raiz** do monorepo (CQ1=A)  
**Projetos Python**: separados (`api/`, `worker/`, `libs/`)

---

## Recursos compartilhados

| Recurso | Spec | Consumidores |
|---|---|---|
| MySQL 8 | DB `lote`, user/senha via env | api, worker |
| Valkey | `:6379` — **DB 0** broker Celery; **DB 1** cache GET | api (broker+cache), worker (broker) |
| Volume `lotes_files` | path container `/data/lotes` | api (write), worker (read) |
| Rede Compose | ex.: `lote-net` | todos |

---

## Contratos de conexão

| Uso | URL / path |
|---|---|
| SQLAlchemy | `mysql+pymysql://...@mysql:3306/lote` |
| Celery broker | `redis://valkey:6379/0` |
| Cache | `redis://valkey:6379/1` |
| Arquivos | `/data/lotes` (`STORAGE_PATH`) |

---

## Regras

1. Não duplicar MySQL/Valkey/volume em composes por projeto.
2. Api e worker **devem** montar o mesmo volume nomeado.
3. Mudanças neste arquivo exigem alinhamento das duas unidades.
4. Esboço AWS futuro não altera estes contratos locais (só troca hosts via env).

---

## Arquivos esperados na raiz (Code Generation)

```text
docker-compose.yml
.env.example
infra/README.md          # esboço Terraform/Copilot (não aplicar)
api/Dockerfile
worker/Dockerfile
```
