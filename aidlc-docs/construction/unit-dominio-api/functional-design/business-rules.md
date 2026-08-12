# Regras de Negócio — unit-dominio-api

## RN-STATUS — Ciclo de vida (lado API)

| ID | Regra |
|---|---|
| RN-S01 | Novo lote inicia sempre em `PENDENTE` |
| RN-S02 | API, no reprocessamento, só permite `ERRO` → `PENDENTE` |
| RN-S03 | API **não** define `PROCESSANDO`, `CONCLUIDO` nem `ERRO` pós-processamento (worker) |
| RN-S04 | `pode_reprocessar()` é verdadeiro **somente** se status == `ERRO` |

## RN-UPLOAD — Entrada do arquivo (US-01)

| ID | Regra |
|---|---|
| RN-U01 | Arquivo obrigatório |
| RN-U02 | Nome deve terminar com `.csv` (case-insensitive recomendado) |
| RN-U03 | Tamanho ≤ 5 MB; senão `TamanhoExcedido` |
| RN-U04 | Cabeçalho e linhas **não** são validados na API |
| RN-U05 | Após persistir lote, arquivo salvo como `{lote_id}_{nome_original}` |

## RN-REPROC — Reprocessamento (US-05)

| ID | Regra |
|---|---|
| RN-R01 | Somente status `ERRO` |
| RN-R02 | Arquivo deve existir no armazenamento; senão erro de domínio e **não** enfileira |
| RN-R03 | Ao reprocessar: status → `PENDENTE`; limpar `erro`; nova task_id |
| RN-R04 | Contagens podem ser zeradas no reset (recomendado para evitar resumo stale) |

## RN-DELETE — Remoção (US-06)

| ID | Regra |
|---|---|
| RN-D01 | Remove registro do repositório em qualquer status, inclusive `PROCESSANDO` |
| RN-D02 | **Não** remove o arquivo do volume |
| RN-D03 | Lote inexistente → `LoteNaoEncontrado` |

## RN-LIST — Listagem (US-04)

| ID | Regra |
|---|---|
| RN-L01 | Ordenação: `criado_em` descendente |
| RN-L02 | Campos mínimos: id, nome_arquivo, status, total_linhas, linhas_validas, linhas_invalidas, criado_em |
| RN-L03 | Sem paginação no MVP |

## RN-ERRO — Modelo de falhas

| Exceção de domínio | Quando | HTTP sugerido (Presentation) |
|---|---|---|
| `LoteNaoEncontrado` | id inexistente | 404 |
| `ArquivoInvalido` | sem arquivo / não `.csv` | 400 |
| `TamanhoExcedido` | > 5 MB | 413 ou 400 |
| `ReprocessamentoNaoPermitido` | status ≠ ERRO | 409 |
| `ArquivoAusenteParaReprocessamento` | reprocessar sem arquivo | 409 ou 422 |
| `TarefaNaoPermitida` | nome fora da allowlist | 400 |

## RN-SHARED — Esboço validadores de linha (libs; detalhe na unit-worker)

| Campo | Esboço |
|---|---|
| nome | obrigatório, não vazio |
| email | formato usuario@dominio.tld |
| cpf | 11 dígitos + DV |
| telefone | opcional; se presente, 10–11 dígitos |

Especificação completa e PBT de linha → **unit-worker-validacao**.

## Mapeamento histórias → regras

| US | Regras |
|---|---|
| US-01 | RN-U*, RN-S01, RN-ERRO upload |
| US-03 | RN-ERRO LoteNaoEncontrado |
| US-04 | RN-L* |
| US-05 | RN-R*, RN-S02, RN-S04 |
| US-06 | RN-D* |
