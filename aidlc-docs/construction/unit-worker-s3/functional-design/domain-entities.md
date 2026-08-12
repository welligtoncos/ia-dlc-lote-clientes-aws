# Entidades / Conceitos — unit-worker-s3

Sem nova entidade de domínio.

## FonteArquivo (lógico)

| Modo | Campos |
|---|---|
| fs | `caminho` (ref relativa) |
| s3 | `bucket`, `chave` (ref) |

## Componentes tocados

| Componente | Mudança |
|---|---|
| `ingerir_clientes` task | kwargs dual |
| `ProcessadorLote` | recebe bytes ou storage+ref |
| `leitor_csv` | API bytes |
| settings worker | validar keys se s3 (Q4=B) |
