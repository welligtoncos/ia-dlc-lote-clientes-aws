# Execução de Testes Unitários

## Escopo

| Suite | Local | Conteúdo |
|---|---|---|
| lote-shared | `libs/tests` | P-API-*, P-VAL-* (Hypothesis) |
| lote-api | `api/tests` | casos de uso + TestClient |
| lote-worker | `worker/tests` | LeitorCsv + ProcessadorLote |

## Executar Testes Unitários

### 1. Executar Todos os Testes Unitários

```bash
pip install -e ./libs -e "./api[dev]" -e "./worker[dev]"
pytest libs/tests api/tests worker/tests -v --import-mode=importlib
```

### 2. Revisar Resultados dos Testes
- **Esperado**: **30** testes passam, 0 falhas (baseline 2026-08-12)
- **Cobertura de Testes**: sem meta formal de coverage % neste MVP; PBT cobre propriedades P-API / P-VAL
- **Localização do Relatório**: stdout do pytest (opcional: `pytest --junitxml=reports/junit.xml`)

### 3. Corrigir Testes com Falha
1. Revise a saída do pytest
2. Isolar suite: `pytest worker/tests -v --import-mode=importlib`
3. Corrija o código / fixtures
4. Reexecute até verde

### Notas
- Use `--import-mode=importlib` para evitar conflito de pacote `tests` entre projetos
- Não requer Docker para a suite unitária (fakes/memória)
