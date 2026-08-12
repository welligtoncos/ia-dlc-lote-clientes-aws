# Métodos dos Componentes — Fase 2 AWS

**Nível**: assinaturas + propósito (regras detalhadas → Functional Design)  
**Decisões**: Q2=A (porta estável) · Q3=A (tradução na infra)

---

## Domain — portas (inalteradas na assinatura)

### `PortaArmazenamentoArquivo`
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `salvar(nome_destino, conteudo)` | str, bytes | str | Persiste e devolve **referência opaca** (path local ou chave lógica S3) |
| `existe(caminho)` | str | bool | Verifica existência da ref (local ou objeto S3) |

### `PortaTarefa`
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `executar(nome_tarefa, payload)` | str, dict | str | Enfileira; payload mínimo `{lote_id, ref}` da Application |

### Demais portas / `Lote`
Sem delta Fase 2.

---

## Application — casos de uso (comportamento)

| Caso | Método | Delta |
|---|---|---|
| IngerirClientes | `executar(nome_arquivo, conteudo)` | Após `salvar`, usa `ref` retornada no payload da task (não interpreta S3) |
| ReprocessarLote | `executar(lote_id)` | Reenfileira com a `ref` já persistida no registro/lote (caminho ou chave) |
| Obter/Listar/Remover | — | Sem delta funcional |

Validadores puros: sem delta (PBT mantido).

---

## Infrastructure — novos / evoluídos

### `ArmazenamentoArquivoS3` (C3b)
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `salvar(nome_destino, conteudo)` | str, bytes | str | `put_object` em `s3://bucket/prefixo/...`; retorna ref (ex.: chave ou URI acordada) |
| `existe(caminho)` | str | bool | `head_object` / equivalent |

### `ArmazenamentoArquivoLocal` (C3a)
Inalterado.

### `criar_armazenamento(...)` (C3c)
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `criar_armazenamento(backend, **cfg)` | str, cfg | PortaArmazenamentoArquivo | `fs` → Local; `s3` → S3 |

### `AdaptadorCelery` (evolução)
| Método | Entrada | Saída | Propósito |
|---|---|---|---|
| `executar(nome, payload)` | str, dict | task_id | Se backend s3: traduz `ref` → kwargs `{lote_id, bucket, chave}`; se fs: `{lote_id, caminho}` |

### Task `ingerir_clientes` (evolução)
| Assinatura cloud | Propósito |
|---|---|
| `ingerir_clientes(lote_id, bucket=None, chave=None, caminho=None)` | Cloud: baixar/ler S3; Local: abrir `caminho`. Nome da task inalterado |

---

## Presentation / Composition Root

| Ponto | Propósito |
|---|---|
| `api` startup | Factory storage + injeção; **sem** middleware API Key |
| `worker` bootstrap | Mesma factory; task registra kwargs dual |
| Rotas `/lotes` | Sem mudança de contrato HTTP |
