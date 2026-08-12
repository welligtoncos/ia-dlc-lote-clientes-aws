# Modelo de Lógica de Negócio — unit-worker-s3

**Decisões**: Q1=A · Q2=A · Q3=A · **Q4=B** · Q5=A · Q6=A

---

## Capacidades

| Capacidade | Descrição |
|---|---|
| Consumir task dual | `caminho` **ou** `bucket`+`chave` |
| Obter bytes | `criar_armazenamento` + `abrir(ref)` |
| Validar / persistir | Inalterado (Fase 1) |
| Retry | 60/120/240; idempotência CONCLUIDO |

---

## Fluxo

```text
Celery kwargs
  |
  +-- caminho=ref  --> backend fs  --> abrir(ref)
  +-- bucket+chave --> backend s3  --> abrir(chave)  [bucket na factory]
  |
  v
bytes CSV --> ler_csv_clientes_de_bytes / TextIO
  |
  v
resumir_validacao --> CONCLUIDO | retry | ERRO
```

## Resolução de modo

- Se `bucket` e `chave` presentes → modo s3  
- Senão se `caminho` presente → modo fs  
- Ambos ou nenhum → erro retentável / configuração inválida
