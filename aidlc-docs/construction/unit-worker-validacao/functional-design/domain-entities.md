# Entidades / Conceitos de Domínio — unit-worker-validacao

## Entidade compartilhada `Lote` (uso pelo worker)

Atributos: ver `unit-dominio-api/.../domain-entities.md`.

### Comportamentos invocados pelo worker

| Método | Pré-condição | Efeito |
|---|---|---|
| `marcar_processando()` | Cabeçalho CSV já validado (RN-S01) | `status = PROCESSANDO` |
| `marcar_concluido(total, validas, invalidas)` | Processamento completo; `total == validas + invalidas` | status CONCLUIDO; contagens; `concluido_em`; limpa `erro` |
| `marcar_erro(mensagem)` | Falha definitiva / retries esgotados | status ERRO; `erro`; `concluido_em` |

### Guard de idempotência (conceito de aplicação)

```text
eh_noop_idempotente(lote, task_id) :=
  lote.status == CONCLUIDO AND lote.celery_task_id == task_id
```

---

## Conceito `LinhaCliente` (não persistido)

| Campo | Tipo lógico | Validação |
|---|---|---|
| nome | texto | RN-F01 |
| email | texto | RN-F02 |
| cpf | texto | RN-F03 (11 dígitos + DV; sem máscara) |
| telefone | texto \| vazio | RN-F04 |

Não há entidade `Cliente` em banco nesta versão — apenas classificação agregada no `Lote`.

---

## Conceito `ResumoValidacao`

| Campo | Invariante |
|---|---|
| total_linhas | ≥ 0; conta só linhas não-branco |
| linhas_validas | ≥ 0 |
| linhas_invalidas | ≥ 0 |
| | `total_linhas = linhas_validas + linhas_invalidas` |

Produzido por função pura sugerida: `resumir_validacao(linhas) → ResumoValidacao`.

---

## Conceito `CabecalhoCsv`

- Colunas esperadas (ordem): `nome`, `email`, `cpf`, `telefone`
- Comparação após remover BOM e trim
- Inválido → falha de processamento (não cria `ResumoValidacao`)

---

## Portas usadas

| Porta | Operações |
|---|---|
| PortaLoteRepositorio | `obter_por_id`, `salvar` |
| (leitura de arquivo) | abrir/ler path do payload — pode ser adapter local no worker sem nova porta de domínio se path já é absoluto no volume |

Worker **não** usa `PortaTarefa` (é consumidor, não produtor).

---

## Exceções / falhas de domínio (lógicas)

| Situação | Tratamento |
|---|---|
| Lote não encontrado | falha → retry → ERRO |
| Arquivo ausente | falha → retry → ERRO |
| Cabeçalho inválido | falha → retry → ERRO (sem PROCESSANDO) |
| Erro I/O / DB no meio | falha tentativa; retry do zero |
| Linha inválida | **não** é exceção — conta em `linhas_invalidas` |

---

## Relacionamentos

```text
Task ingerir_clientes
  → Lote (MySQL)
  → Arquivo CSV (volume)
  → validadores (lote-shared) → classificação LinhaCliente
  → ResumoValidacao → Lote.marcar_concluido | marcar_erro
```

---

## Propriedades PBT ligadas

P-VAL-01..07 — ver `business-logic-model.md`.
