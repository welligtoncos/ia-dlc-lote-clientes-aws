# Code Generation Summary — unit-api-cloud

**Historias**: US-AWS-01, US-AWS-02, US-AWS-04

## Modificado
- `api/.../adapters.py` — tradução kwargs fs/s3
- `api/.../casos_uso.py` — payload `{lote_id, ref}`
- `api/.../main.py` — wiring backend/bucket no adapter
- `api/.../settings.py` — validacao AWS keys se s3 (Q6=B)
- `.env.example`

## Criado
- `api/tests/test_adaptador_celery_kwargs.py`
