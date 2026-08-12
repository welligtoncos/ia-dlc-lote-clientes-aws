# Mapa História → Unidade

| História | Título | Unidade primária | Unidade suporte | Prioridade |
|---|---|---|---|---|
| US-01 | Enviar lote CSV e receber confirmação assíncrona | unit-dominio-api | unit-worker-validacao (processa depois) | Must |
| US-02 | Processar e validar CSV em background | unit-worker-validacao | libs/validacao | Must |
| US-03 | Consultar status e resumo de um lote | unit-dominio-api | — | Must |
| US-04 | Listar ingestões realizadas | unit-dominio-api | — | Must |
| US-05 | Reprocessar lote em erro | unit-dominio-api | unit-worker-validacao | Must |
| US-06 | Remover registro de ingestão | unit-dominio-api | — | Must |

## Cobertura

- **Todas as histórias atribuídas**: Sim (US-01..06)
- **unit-dominio-api**: US-01, US-03, US-04, US-05, US-06
- **unit-worker-validacao**: US-02 (+ execução de US-01/US-05)

## Ordem sugerida na Construction

1. `unit-dominio-api` — contratos `libs/`, API, enqueue  
2. `unit-worker-validacao` — task, validação, conclusão do lote
