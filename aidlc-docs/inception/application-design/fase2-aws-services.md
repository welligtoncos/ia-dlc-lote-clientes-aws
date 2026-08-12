# Serviços e Orquestração — Fase 2 AWS

**Decisões**: Q3=A · Q4=A · Q6=A

---

## Serviços de aplicação (inalterados na orquestração lógica)

| Serviço | Orquestra | Delta cloud |
|---|---|---|
| IngerirClientes | validar upload → storage.salvar → repo → tarefa.executar(ref) | Storage pode ser S3; task kwargs traduzidos na infra |
| ObterLote / ListarLotes / RemoverLote | como Fase 1 | Via Gateway+Key no edge |
| ReprocessarLote | existe(ref) → enfileira | `existe` S3 ou fs |

---

## Serviço de processamento (worker)

| Serviço | Orquestra | Delta |
|---|---|---|
| Task `ingerir_clientes` | PROCESSANDO → ler CSV → validação → CONCLUIDO/ERRO | Fonte do CSV: S3 (`bucket`+`chave`) ou filesystem (`caminho`) |

---

## Composition / seleção de backend

```text
Env STORAGE_BACKEND=fs|s3
        |
        v
  criar_armazenamento()   (Composition Root)
        |
        +-- fs --> ArmazenamentoArquivoLocal
        +-- s3 --> ArmazenamentoArquivoS3
        |
        v
  Casos de Uso (agnósticos)
```

---

## Fluxo cloud (ponta a ponta)

```text
Client + API Key
    -> API Gateway
    -> ALB -> ECS api (Presentation)
    -> IngerirClientes
    -> PortaArmazenamento --> S3
    -> PortaTarefa --> AdaptadorCelery
         traduz ref -> {lote_id, bucket, chave}
    -> ElastiCache
    -> ECS worker
         le S3, valida, atualiza RDS
```

## Fluxo local (Compose)

```text
Client
    -> FastAPI local
    -> IngerirClientes
    -> ArmazenamentoArquivoLocal (volume)
    -> Celery kwargs {lote_id, caminho}
    -> worker local
```

---

## Autenticação

- API Key: **somente API Gateway** (Q4=A)
- ECS api confia no tráfego ALB (SG privado)
- Sem serviço de auth dentro da Application neste ciclo
