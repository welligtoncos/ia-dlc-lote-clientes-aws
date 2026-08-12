# Serviços e Orquestração

**Decisão Q4=A**: um caso de uso por operação de API (não um “god service”).

---

## Serviços de aplicação (casos de uso)

| Serviço | Orquestra | Portas usadas | Dispara fila? |
|---|---|---|---|
| IngerirClientes | Validação mínima de entrada (.csv, tamanho) → salvar arquivo → criar Lote PENDENTE → PortaTarefa.executar | Armazenamento, Repositório, Tarefa | Sim |
| ObterLote | Buscar por id; 404 se ausente | Repositório | Não |
| ListarLotes | Listar todos | Repositório | Não |
| ReprocessarLote | Obter lote → `pode_reprocessar` → reset status → enfileirar | Repositório, Tarefa (+ existe arquivo) | Sim |
| RemoverLote | Remover no MySQL; não apaga arquivo | Repositório | Não |

---

## Serviço de processamento (worker)

| Serviço | Orquestra | Notas |
|---|---|---|
| Task ingerir_clientes | Carregar lote → PROCESSANDO → ler CSV → `resumir_validacao` → CONCLUIDO ou retry/ERRO | Vive na Infrastructure; chama validadores da Application |

---

## Padrão de orquestração

```text
HTTP (Presentation)
        |
        v
  Caso de Uso (Application)
        |
        +---> PortaArmazenamentoArquivo --> Adapter Local
        +---> PortaLoteRepositorio ------> LoteRepositorio / MySQL
        +---> PortaTarefa ---------------> AdaptadorCelery --> Valkey
                                                    |
                                                    v
                                            Worker Task
                                                    |
                                                    +--> validadores Application
                                                    +--> PortaLoteRepositorio
```

---

## Coordenação API ↔ Worker

1. API responde 202 assim que a mensagem é enfileirada (fire-and-forget).
2. Worker é a única escrita de resumo/contagens e de CONCLUIDO/ERRO após processamento.
3. Status canônico sempre no MySQL via repositório.
