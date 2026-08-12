# Entidades / Conceitos de Domínio — unit-libs-storage

Esta unidade **não** introduz entidade de negócio nova (`Lote` permanece). Conceitos:

---

## ReferenciaArmazenamento (value object lógico)

| Campo | Tipo | Descrição |
|---|---|---|
| valor | str | Chave relativa opaca (`lotes/{lote_id}_{nome}`) |

Invariantes: não vazia; não começa com `/` nem `s3://`; usa `/` como separador.

---

## ConfiguracaoArmazenamento (value object)

| Campo | fs | s3 |
|---|---|---|
| backend | `fs` | `s3` |
| diretorio_base | obrigatório | N/A |
| bucket | N/A | obrigatório |
| region | N/A | opcional (default SDK) |
| prefixo | default `lotes/` | default `lotes/` |

---

## Exceções (em `lote_shared.domain.excecoes` ou módulo storage)

| Tipo | Hierarquia sugerida |
|---|---|
| `ObjetoNaoEncontrado` | domínio / storage |
| `ErroArmazenamento` | domínio / storage |

---

## Porta (contrato)

`PortaArmazenamentoArquivo`: `salvar`, `existe`, `abrir` — implementações Local e S3 em `libs`.

## Relação com Lote

- `Lote` continua a guardar o que a Application persistir (hoje tipicamente caminho; na Fase 2 a **ref relativa**).
- Migração de registros antigos com path absoluto: fora do escopo mínimo; Compose novo usa refs relativas.
