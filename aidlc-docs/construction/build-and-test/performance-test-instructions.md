# Instruções de Testes de Desempenho

## Propósito
Orientar validação leve de desempenho no MVP local. **Não há SLO formal de worker** (NFR best-effort); API tem metas soft de p95.

## Requisitos de Desempenho (herdados)

| ID | Meta |
|---|---|
| NFR-PERF-01 | `POST /lotes` p95 **&lt; 300 ms** (arquivo ≤ 5 MB; sem parse na API) |
| NFR-PERF-02 | GET lotes p95 **&lt; 200 ms** (MVP, poucos milhares de lotes) |
| NFR-PERF-W01 | Processamento CSV ≤ 5 MB: best-effort (minutos OK) |
| NFR-SCALE-01 | Carga MVP **&lt; 10 req/min**; 1 api + worker concurrency=2 |

## Configurar Ambiente

```bash
docker compose up -d --build
```

## Executar (smoke de latência — opcional)

### 1. Latência de POST (exemplo PowerShell)

```powershell
Measure-Command { curl.exe -s -X POST http://localhost:8000/lotes -F "arquivo=@fixtures/clientes.csv" }
```

Repita ~10 vezes e estime p95 manualmente. Meta soft: &lt; 300 ms na máquina de dev.

### 2. Latência de GET

```powershell
Measure-Command { curl.exe -s http://localhost:8000/lotes/1 }
```

### 3. Carga formal
- **Status**: **N/A neste ciclo** — sem JMeter/k6 obrigatório (carga &lt; 10 req/min)
- Se necessário no futuro: script k6 contra `POST /lotes` e `GET /lotes/{id}`

## Analisar Resultados
- Comparar com NFR-PERF-* acima
- Gargalos esperados: disco do volume, MySQL no compose, Valkey local
- Worker: tempo de parse é secundário ao MVP

## Otimização
Só se metas soft da API forem sistematicamente violadas em hardware típico de desenvolvimento.
