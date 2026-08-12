# Componentes Lógicos NFR — unit-worker-validacao

Componentes **lógicos** (detalhe de compose/Dockerfile → Infrastructure Design).

---

## Diagrama lógico

```text
  Valkey broker (DB0)
          |
          v
  +------------------+
  | CeleryApp        |
  | concurrency=2    |
  | acks_late, pref=1|
  +--------+---------+
           |
           v
  +------------------+
  | TaskIngerir      |
  | Clienteles       |
  | (autoretry)      |
  +--------+---------+
           |
     +-----+------+------------+-------------+
     |            |            |             |
     v            v            v             v
 +--------+  +---------+  +----------+  +-----------+
 |Settings|  |LeitorCsv|  |Servico   |  |LoteRepo   |
 |fail-   |  |stream   |  |Validacao |  |(shared)   |
 |fast    |  |BOM/hdr  |  |(shared   |  +-----+-----+
 +--------+  +---------+  | valid.)  |        |
                          +----------+        v
                                      +-------------+
                                      | MySQL       |
                                      +-------------+
           |
           +----> JsonLogger (task_id, lote_id, tentativa)
           |
           +----> CacheInvalidator --> Valkey DB1 (lote:{id}, lista)
```

### Text alternative
CeleryApp consome Valkey DB0; TaskIngerirClientes orquestra Settings, LeitorCsv, ServicoValidacao, LoteRepo (MySQL), JsonLogger e CacheInvalidator (Valkey DB1).

---

## Catálogo de componentes

| Componente | Responsabilidade NFR | Depende de |
|---|---|---|
| **CeleryApp** | Broker URL; concurrency=2; acks_late; prefetch=1; sem result backend | Settings, Valkey DB0 |
| **TaskIngerirClientes** | Orquestra fluxo F-W1; autoretry; guard idempotente; marca status | todos abaixo |
| **Settings** | Fail-fast env (`DATABASE_URL`, `CELERY_BROKER_URL`, `STORAGE_PATH`) | env |
| **LeitorCsv** | UTF-8+BOM; valida cabeçalho; itera linhas; ignora em branco | STORAGE_PATH / caminho payload |
| **ServicoValidacao** | Aplica validadores `lote-shared`; produz `ResumoValidacao` | lote-shared.validacao |
| **LoteRepo** | obter/salvar Lote (status/contagens) | lote-shared.persistence, MySQL |
| **CacheInvalidator** | DEL `lote:{id}` (+ lista) após CONCLUIDO/ERRO | Valkey DB1 / CACHE_URL |
| **JsonLogger** | Logs estruturados com correlação task | — |

---

## Fluxo de integração (resumo)

| Etapa | Componentes |
|---|---|
| Boot | Settings → CeleryApp |
| Mensagem | CeleryApp → TaskIngerirClientes |
| NOOP | Task + LoteRepo (guard) + JsonLogger |
| Header OK | LeitorCsv → Task → LoteRepo.marcar_processando |
| Parse | LeitorCsv → ServicoValidacao → resumo em memória |
| Sucesso | LoteRepo.marcar_concluido → CacheInvalidator → JsonLogger |
| Falha terminal | LoteRepo.marcar_erro → CacheInvalidator → JsonLogger |
| Falha retentável | JsonLogger → Celery autoretry (sem marcar_erro) |

---

## Fora destes componentes

- FastAPI / Presentation → unit-dominio-api
- Provisionamento AWS → fora do MVP local
- Detalhe de redes/volumes compose → Infrastructure Design
