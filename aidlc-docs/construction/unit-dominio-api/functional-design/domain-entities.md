# Entidades de Domínio — unit-dominio-api

## Entidade `Lote`

| Atributo | Tipo lógico | Obrigatório | Notas |
|---|---|---|---|
| id | identificador | sim (após persistir) | gerado pelo repositório |
| nome_arquivo | texto | sim | nome original do upload |
| caminho_arquivo | texto | sim após salvar | path no volume (`{id}_{nome}`) |
| status | enumeração | sim | PENDENTE \| PROCESSANDO \| CONCLUIDO \| ERRO |
| total_linhas | inteiro ≥ 0 | sim | default 0 |
| linhas_validas | inteiro ≥ 0 | sim | default 0 |
| linhas_invalidas | inteiro ≥ 0 | sim | default 0 |
| erro | texto \| nulo | não | preenchido em ERRO |
| celery_task_id | texto \| nulo | não | última task enfileirada |
| criado_em | data/hora | sim | |
| concluido_em | data/hora \| nulo | não | worker preenche |

### Comportamentos

| Método | Pré-condição | Efeito |
|---|---|---|
| `criar_pendente(nome_arquivo)` | nome não vazio | status=PENDENTE, totais=0 |
| `preparar_reprocessamento()` | status=ERRO | status=PENDENTE; erro=nulo; totais→0; concluido_em=nulo |
| `pode_reprocessar()` | — | true iff status=ERRO |
| `associar_task(task_id)` | — | celery_task_id=task_id |

> Métodos `marcar_processando` / `marcar_concluido` / `marcar_erro` existem na entidade compartilhada para o **worker**; a API não os invoca (RN-S03).

### Invariantes
- `linhas_validas + linhas_invalidas == total_linhas` quando status=CONCLUIDO (garantido pelo worker; API não calcula)
- status ∈ {PENDENTE, PROCESSANDO, CONCLUIDO, ERRO}

---

## Enumeração `StatusLote`

`PENDENTE` | `PROCESSANDO` | `CONCLUIDO` | `ERRO`

---

## Portas (contratos de domínio)

### PortaLoteRepositorio
- `salvar(lote) → lote`
- `obter_por_id(id) → lote | nulo`
- `listar_ordenados_por_criacao_desc() → lista[lote]`
- `remover(id) → bool`

### PortaArmazenamentoArquivo
- `salvar(nome_destino, conteudo) → caminho`
- `existe(caminho) → bool`

### PortaTarefa
- `executar(nome_tarefa, payload) → task_id`  
  - rejeita nome fora da allowlist (`TarefaNaoPermitida`)

---

## Exceções de domínio

Hierarquia sugerida: `ErroDominioLote` ← concretas listadas em business-rules.md.

---

## Relacionamentos

```text
Lote 1 -- usa --> PortaLoteRepositorio
Lote (path) -- referenciado por --> PortaArmazenamentoArquivo
Casos de uso -- dependem de --> 3 portas
```

Não há entidade `Cliente` persistida nesta versão (só agregação no worker).

---

## Propriedades PBT ligadas à entidade

- P-API-01, P-API-02 (ver business-logic-model.md)
