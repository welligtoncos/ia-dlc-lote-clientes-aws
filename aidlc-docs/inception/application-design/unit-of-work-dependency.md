# Dependências entre Unidades de Trabalho

## Matriz (projetos Python)

| De \ Para | lote-api | lote-worker | lote-shared |
|---|---|---|---|
| lote-api (`unit-dominio-api`) | — | Não (só via fila) | Depende (path/editable) + ownership |
| lote-worker (`unit-worker-validacao`) | Não | — | Depende (path/editable) |
| lote-shared (`libs/`) | — | — | — |

**Proibido**: `import lote_api` dentro de `lote_worker` (e o inverso).

## Grafo

```text
lote-api  ----pip/path----> lote-shared <----pip/path----  lote-worker
    |                                                        ^
    |  Celery apply_async {lote_id, caminho}                 |
    +--------------------> Valkey ----------------------------+
    |                                                        |
    +---- grava CSV ----> Volume compartilhado <--- le CSV --+
    |                                                        |
    +---- MySQL via lote_shared.persistence -----------------+
```

## Integração entre projetos

| Canal | Contrato |
|---|---|
| Pacote Python | `lote-shared` versionado no monorepo |
| Fila | task allowlisted + payload `{lote_id, caminho}` |
| Volume | mesmo path montado nas duas imagens |
| MySQL | schema `lotes` via persistence compartilhada |

## Ordem Construction / build
1. Publicar/instalar `lote-shared`
2. Construir `lote-api`
3. Construir `lote-worker`
