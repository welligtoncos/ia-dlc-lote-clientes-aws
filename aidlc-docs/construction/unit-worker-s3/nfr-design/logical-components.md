# Componentes Lógicos — unit-worker-s3

**Decisão Q5=A**: evoluir task + processador; sem `ResolvedorArmazenamento` com DI formal.

---

```text
Celery broker
      |
      v
Task ingerir_clientes(lote_id, caminho=?, bucket=?, chave=?)
      |
      +-- validar modo (fs xor s3)
      |
      v
criar_armazenamento()  (lote_shared)
      |
      v
PortaArmazenamento.abrir(ref)  -->  bytes
      |
      v
ler_csv_clientes_de_bytes / TextIO
      |
      v
Processador (validadores + MySQL)  -- inalterado RN-B*
```

## Task `ingerir_clientes`

| Responsabilidade | Detalhe |
|---|---|
| Assinatura dual | `caminho` **ou** (`bucket` + `chave`) |
| Resolução | Montar `ref` + factory conforme modo |
| Retry | Decorators Celery existentes |

## Processador / I/O

| Responsabilidade | Detalhe |
|---|---|
| Abrir via lib | Sem boto3 direto |
| Parse | Helper bytes (utf-8-sig) |
| Domínio | Validação + persistência inalteradas |

## Bootstrap segurança

| Check | Ação |
|---|---|
| `STORAGE_BACKEND=s3` | Exigir `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |

## Fora desta unit

ECS task def · Secrets Manager wiring · ElastiCache — `unit-infra-aws`.
