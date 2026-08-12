# Modelo de Lógica de Negócio — unit-libs-storage

**Decisões**: Q1–Q8 = A  
**Escopo**: dual storage (fs/s3), referência opaca, factory, leitura via porta

---

## Capacidades

| Capacidade | Descrição |
|---|---|
| Persistir bytes | Gravar conteúdo e devolver **ref relativa** |
| Verificar existência | `existe(ref)` sem carregar o corpo |
| Abrir conteúdo | `abrir(ref)` → bytes (worker/API sem SDK direto) |
| Selecionar backend | Factory por `STORAGE_BACKEND` ∈ {`fs`, `s3`} |

---

## Fluxo — salvar

```text
Entrada: nome_logico (ex. "{lote_id}_{nome_original}"), conteudo: bytes
    |
    v
Montar chave relativa: "lotes/" + nome_logico   (prefixo padrao)
    |
    +-- backend fs: escrever sob diretorio_base / chave
    +-- backend s3: put_object(bucket, Key=chave, Body=conteudo)
    |
    v
Retorno: ref = chave relativa (ex. "lotes/12_clientes.csv")
         NUNCA incluir bucket nem path absoluto na ref (Q1=A)
```

## Fluxo — existe / abrir

```text
Entrada: ref (chave relativa)
    |
    +-- fs: Path(diretorio_base / ref)
    |         existe -> is_file()
    |         abrir  -> read_bytes(); se ausente -> ObjetoNaoEncontrado
    |
    +-- s3: Key = ref (bucket da config)
              existe -> head_object; 404/NotFound -> False; outros erros propagam como ErroArmazenamento
              abrir  -> get_object body; NotFound -> ObjetoNaoEncontrado
```

## Fluxo — factory

```text
criar_armazenamento(backend, **cfg)
  backend "fs" (default se vazio/None) -> ArmazenamentoArquivoLocal(diretorio_base)
  backend "s3" -> ArmazenamentoArquivoS3(bucket, region, prefixo opcional)
  outro -> ErroArmazenamento / ValueError de configuracao
```

---

## Contratos (lógicos)

### PortaArmazenamentoArquivo (evolução)
| Método | In | Out |
|---|---|---|
| `salvar(nome_destino, conteudo)` | str, bytes | str (ref relativa) |
| `existe(ref)` | str | bool |
| `abrir(ref)` | str | bytes | **novo (Q7=A)** |

`nome_destino` na chamada do caso de uso permanece `{lote_id}_{nome_original}`; o adapter aplica prefixo `lotes/`.

---

## Fora desta unidade

- Tradução kwargs Celery `{bucket, chave}` vs `{caminho}` → unit-api-cloud / unit-worker-s3  
- IAM, bucket policy, Terraform → unit-infra-aws  
- Validação de linhas CSV → já em libs validacao / worker
