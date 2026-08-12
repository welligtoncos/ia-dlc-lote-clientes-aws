# Padrões NFR — unit-libs-storage

**Decisões**: Q1=A · Q2=A · Q3=B · Q4=A · Q5=A · Q6=A

---

## Resiliência — Fail-fast (Q1=A)

| Padrão | Aplicação |
|---|---|
| Fail-fast | Erros OS/SDK → `ErroArmazenamento` ou `ObjetoNaoEncontrado` |
| Sem circuit breaker | Na lib |
| Sem retry loop | Retries no Celery / defaults mínimos do SDK |

## Escalabilidade (Q2=A)

| Padrão | Aplicação |
|---|---|
| Instância por processo | Factory cria adapter no composition root de api/worker |
| Sem singleton global de módulo | Evita estado oculto entre testes |

## Desempenho — Streaming (Q3=B)

| Padrão | Aplicação |
|---|---|
| Streaming I/O | S3: `upload_fileobj` / `download_fileobj` (ou Body file-like); fs: write/read via buffer |
| Multipart | Habilitar TransferConfig com threshold ≥ 5 MB (objetos do produto ≤ 5 MB usam single-part stream na prática) |
| Contrato porta | `salvar`/`abrir` ainda expõem `bytes` na borda da porta (Functional Design); streaming é detalhe interno do adapter |

## Segurança (Q4=A)

| Padrão | Aplicação |
|---|---|
| Credential chain | Sem keys no código |
| Validação na construção | `ArmazenamentoArquivoS3` exige `bucket` não vazio; senão `ErroArmazenamento` |
| Client injetável | **Não** exigido neste ciclo (Q4≠B); testes usam moto no client default / env |

## Mapeamento NFR → padrão

| NFR | Padrão |
|---|---|
| NFR-LIB-AVAIL-01 | Fail-fast |
| NFR-LIB-SCALE-02 | Instância por processo |
| NFR-LIB-PERF-* | Streaming interno |
| NFR-LIB-SEC-01 | Credential chain + validação bucket |
