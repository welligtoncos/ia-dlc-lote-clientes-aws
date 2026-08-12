# Regras de Negócio — unit-libs-storage

## RN-REF — Referência opaca (Q1=A)

| ID | Regra |
|---|---|
| RN-REF01 | `salvar` retorna **apenas** chave relativa (ex.: `lotes/123_arq.csv`) |
| RN-REF02 | Ref **não** contém `s3://`, bucket, nem path absoluto de filesystem |
| RN-REF03 | Bucket / `diretorio_base` / region vivem só na configuração do adapter |
| RN-REF04 | `existe` e `abrir` recebem a mesma ref devolvida por `salvar` |

## RN-NOME — Convenção de objeto (Q2=A)

| ID | Regra |
|---|---|
| RN-N01 | Nome lógico = `{lote_id}_{nome_original}` (como Fase 1 no caso de uso) |
| RN-N02 | Chave persistida = `lotes/` + nome lógico (prefixo padrão) |
| RN-N03 | Prefixo configurável na factory/config, default `lotes/` |

## RN-FS — Backend filesystem

| ID | Regra |
|---|---|
| RN-FS01 | Default quando `STORAGE_BACKEND` ausente ou `fs` |
| RN-FS02 | Arquivos sob `diretorio_base` espelhando a chave relativa |
| RN-FS03 | `ArmazenamentoArquivoLocal` **consolida-se em `libs`** (Q3=A); api remove implementação própria e importa da lib |
| RN-FS04 | `existe`: True somente se arquivo regular presente |
| RN-FS05 | `abrir`: lê bytes; se ausente → `ObjetoNaoEncontrado` |

## RN-S3 — Backend S3

| ID | Regra |
|---|---|
| RN-S301 | Ativo somente se `STORAGE_BACKEND=s3` e bucket configurado |
| RN-S302 | `salvar` → put_object com Key = ref relativa |
| RN-S303 | `existe` → head_object; 404/NotFound → False; demais erros → `ErroArmazenamento` (Q4=A) |
| RN-S304 | `abrir` → get_object; NotFound → `ObjetoNaoEncontrado`; demais → `ErroArmazenamento` |
| RN-S305 | Credenciais via chain padrão AWS (env/task role); **sem** secrets no código |

## RN-FACTORY — Seleção de backend (Q6=A)

| ID | Regra |
|---|---|
| RN-F01 | Valores aceitos: `fs`, `s3` (case-sensitive recomendado lower) |
| RN-F02 | Default: `fs` |
| RN-F03 | Valor desconhecido → erro explícito na factory (não fallback silencioso) |
| RN-F04 | Sem aliases (`filesystem`, `local`, etc.) neste ciclo |

## RN-ERRO — Exceções de domínio (Q5=A)

| Exceção | Quando |
|---|---|
| `ObjetoNaoEncontrado` | `abrir` com ref inexistente |
| `ErroArmazenamento` | Falha de I/O/SDK relevante (perm, rede, config s3 incompleta) |
| (factory) | Backend inválido |

## Mapeamento histórias

| US | Regras |
|---|---|
| US-AWS-02 | RN-REF*, RN-N*, RN-S3*, RN-FACTORY, RN-ERRO |
| US-AWS-04 | RN-FS*, RN-FACTORY default fs |
