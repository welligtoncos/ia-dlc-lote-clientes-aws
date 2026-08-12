# Entidades / Conceitos — unit-api-cloud

Sem nova entidade de domínio. Conceitos de integração:

---

## PayloadMinimoTarefa (lógico)

| Campo | Tipo | Descrição |
|---|---|---|
| lote_id | int | ID do lote |
| ref | str | Chave relativa de armazenamento |

Produzido pela Application; consumido pelo AdaptadorCelery.

---

## KwargsFs

| Campo | Tipo |
|---|---|
| lote_id | int |
| caminho | str (ref relativa) |

## KwargsS3

| Campo | Tipo |
|---|---|
| lote_id | int |
| bucket | str |
| chave | str (ref relativa) |

---

## Relação com `Lote`

- `Lote.caminho_arquivo` armazena a **ref** (não path absoluto / não `s3://`)
- Campo de nome permanece por compatibilidade de schema; semanticamente é a ref

## Componentes tocados

| Componente | Mudança |
|---|---|
| `CasoUsoIngerirClientes` / `ReprocessarLote` | Payload mínimo `{lote_id, ref}` (ou manter chave `caminho` no dict interno se adapter aceitar alias `ref`) |
| `AdaptadorCelery` | Tradução + config backend/bucket |
| Presentation | Sem delta de auth |
