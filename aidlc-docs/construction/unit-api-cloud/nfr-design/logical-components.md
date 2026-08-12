# Componentes Lógicos — unit-api-cloud

**Decisão Q5=A**: evoluir `AdaptadorCelery` + wiring; sem `TradutorTarefa` separado.

---

```text
Presentation (FastAPI)
        |
        v
Casos de Uso  --payload {lote_id, ref}-->  PortaTarefa
        |                                      |
        |                                      v
        |                              AdaptadorCelery
        |                                |-- fs -> {lote_id, caminho}
        |                                +-- s3 -> {lote_id, bucket, chave}
        |                                      |
        +--> criar_armazenamento()             v
                    (libs)                  Celery broker
```

## AdaptadorCelery (evolução)

| Responsabilidade | Detalhe |
|---|---|
| Allowlist | `ingerir_clientes` |
| Tradução | `ref` → kwargs conforme `storage_backend` |
| Config | `broker_url`, `storage_backend`, `s3_bucket` |
| Erros | Propagar; caso de uso degrada |

## Casos de uso (delta mínimo)

| Caso | Mudança |
|---|---|
| Ingerir / Reprocessar | Passar `ref` (valor de `caminho_arquivo`) no payload mínimo |

## Fora desta unit

Worker dual kwargs · Gateway · ECS — units seguintes.
