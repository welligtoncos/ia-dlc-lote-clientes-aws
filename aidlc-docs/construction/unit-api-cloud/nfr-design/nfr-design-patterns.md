# Padrões NFR — unit-api-cloud

**Decisões**: Q1–Q6 = A

---

## Resiliência — Degrade (Q1=A)

| Padrão | Aplicação |
|---|---|
| Degrade on enqueue failure | Caso de uso captura Exception; lote `PENDENTE` |
| Fail-propagate no adapter | AdaptadorCelery não engole erros do broker |

## Escalabilidade (Q2=A)

| Padrão | Aplicação |
|---|---|
| Client por processo | `AdaptadorCelery` instanciado no composition root |

## Desempenho (Q3=A)

| Padrão | Aplicação |
|---|---|
| Tradução in-memory | if `fs`/`s3` monta kwargs; sem head/get S3 na API |

## Segurança (Q4=A)

| Padrão | Aplicação |
|---|---|
| Sem secrets no payload | kwargs só `lote_id` + `caminho` ou `bucket`+`chave` |
| Credenciais S3 | Só no worker (task role), não na API |

## Mapeamento NFR → padrão

| NFR | Padrão |
|---|---|
| NFR-API-AVAIL-* | Degrade |
| NFR-API-PERF-02 | Tradução in-memory |
| NFR-API-SEC-* | Sem keys no payload; sem auth app |
