# Métodos dos Componentes

**Nível de detalhe**: Q6=A — assinaturas + tipos + propósito de uma linha.  
Regras detalhadas → Functional Design.

Convenção: português nos identificadores (RNF-09).

---

## Domain

### Entidade `Lote`
| Método / fábrica | Entrada | Saída | Propósito |
|---|---|---|---|
| `criar_pendente(nome_arquivo)` | str | Lote | Cria lote com status PENDENTE |
| `marcar_processando()` | — | — | Transita PENDENTE→PROCESSANDO |
| `marcar_concluido(total, validas, invalidas)` | int, int, int | — | Grava resumo e CONCLUIDO |
| `marcar_erro(mensagem)` | str | — | Define ERRO + mensagem |
| `pode_reprocessar()` | — | bool | True somente se status == ERRO |

### `PortaTarefa` (interface)
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `executar(nome_tarefa, payload)` | str, dict | str (task_id) | Enfileira tarefa allowlisted |
| `obter_status(task_id)` | str | str | Consulta status da task (auxiliar; fonte canônica = MySQL) |

### `PortaLoteRepositorio` (interface)
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `salvar(lote)` | Lote | Lote | Insere/atualiza lote |
| `obter_por_id(id)` | int | Lote \| None | Busca por id |
| `listar()` | — | list[Lote] | Lista todos |
| `remover(id)` | int | bool | Remove registro |

### `PortaArmazenamentoArquivo` (interface)
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `salvar(nome_original, conteudo)` | str, bytes/stream | str (caminho) | Persiste no volume compartilhado |
| `existe(caminho)` | str | bool | Verifica existência para reprocessamento |

---

## Application

### Validação (funções puras — PBT)
| Função | Entrada | Saída | Propósito |
|---|---|---|---|
| `validar_nome(valor)` | str \| None | bool | nome obrigatório não vazio |
| `validar_email(valor)` | str \| None | bool | formato email |
| `validar_cpf(valor)` | str \| None | bool | 11 dígitos + DV |
| `validar_telefone(valor)` | str \| None | bool | vazio OK; senão 10–11 dígitos |
| `validar_linha(registro)` | dict | bool | conjunção das regras |
| `resumir_validacao(linhas)` | iterable[dict] | (total, validas, invalidas) | agrega contagens |

### Casos de uso
| Caso de uso | Método | Entrada | Saída | Propósito |
|---|---|---|---|---|
| IngerirClientes | `executar(nome_arquivo, conteudo)` | str, bytes | {lote_id, task_id, status} | Cria lote, salva arquivo, enfileira |
| ObterLote | `executar(lote_id)` | int | Lote \| erro | Consulta por id |
| ListarLotes | `executar()` | — | list[Lote] | Lista ingestões |
| ReprocessarLote | `executar(lote_id)` | int | {lote_id, task_id, status} \| erro | Reenfileira se ERRO |
| RemoverLote | `executar(lote_id)` | int | ok \| erro | Remove registro MySQL |

---

## Infrastructure

| Adapter | Métodos-chave | Propósito |
|---|---|---|
| AdaptadorCelery | `executar`, `obter_status` | Implementa PortaTarefa + allowlist |
| Task `ingerir_clientes` | `run(lote_id, caminho)` | Lê CSV, chama validação Application, atualiza lote |
| LoteRepositorio | CRUD conforme porta | Persistência MySQL |
| ArmazenamentoArquivoLocal | `salvar`, `existe` | Volume compartilhado |
| celery_app | config broker/backend | Conexão Valkey |

---

## Presentation

| Rota | Handler | Entrada | Saída HTTP | Propósito |
|---|---|---|---|---|
| POST /lotes | `criar_lote` | multipart file | 202 + body | US-01 |
| GET /lotes | `listar_lotes` | — | 200 lista | US-04 |
| GET /lotes/{id} | `obter_lote` | path id | 200 / 404 | US-03 |
| PUT /lotes/{id} | `reprocessar_lote` | path id | 202 / 4xx | US-05 |
| DELETE /lotes/{id} | `remover_lote` | path id | 204 / 404 | US-06 |
