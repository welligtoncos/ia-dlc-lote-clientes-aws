# Task summary — unit-worker-validacao

- `ProcessadorLote` em `worker/src/lote_worker/application/processador.py`
- Task Celery `ingerir_clientes` (nome allowlist API)
- `LeitorCsv` (BOM, header, ignora blank), `CacheInvalidator` (Valkey DB1)
- Retry countdown 60/120/240; `marcar_erro` ao esgotar
- Testes: `worker/tests/test_leitor_csv.py`, `test_processador.py`
