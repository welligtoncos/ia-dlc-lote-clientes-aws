# Componentes — Serviço de Ingestão de Clientes

**Decisões**: Q1=A (4 camadas) · Q2=B (validação na Application) · Q3=A · Q5=A

---

## C1 — Domain

| Campo | Descrição |
|---|---|
| **Propósito** | Núcleo do negócio sem dependência de frameworks |
| **Responsabilidades** | Entidade `Lote` e ciclo de status; portas `PortaTarefa`, `PortaLoteRepositorio`, `PortaArmazenamentoArquivo` |
| **Não faz** | I/O, HTTP, Celery, SQL, parsing de CSV |
| **Interfaces** | Modelos de domínio; contratos das portas |
| **Histórias** | Base para US-01..06 |

---

## C2 — Application

| Campo | Descrição |
|---|---|
| **Propósito** | Orquestrar casos de uso da API e regras de validação de linha |
| **Responsabilidades** | Casos de uso: IngerirClientes, ObterLote, ListarLotes, ReprocessarLote, RemoverLote; validadores puros (nome, email, cpf, telefone); coordenar portas |
| **Não faz** | Detalhes de Celery/SQL/filesystem; rotas HTTP |
| **Interfaces** | Métodos públicos dos casos de uso; funções de validação (PBT) |
| **Histórias** | US-01..06 (orquestração); US-02 (regras de validação) |

> **PBT**: embora a validação pertença à Application (Q2=B), as funções devem ser **puras** (sem I/O) para testes baseados em propriedades.

---

## C3 — Infrastructure

| Campo | Descrição |
|---|---|
| **Propósito** | Adaptadores concretos das portas |
| **Responsabilidades** | `AdaptadorCelery` + allowlist + tasks; `LoteRepositorio` (SQLAlchemy/MySQL); `ArmazenamentoArquivoLocal` (volume compartilhado); `celery_app` (Valkey) |
| **Não faz** | Regras de negócio / validação de linha |
| **Interfaces** | Implementações das portas do Domain |
| **Histórias** | US-01, US-02, US-05 (fila); persistência em todas |

---

## C4 — Presentation

| Campo | Descrição |
|---|---|
| **Propósito** | Expor HTTP/OpenAPI e traduzir request/response |
| **Responsabilidades** | Rotas `/lotes`; upload multipart; status codes (202, 200, 204, 4xx); DTOs de resposta |
| **Não faz** | Persistência, enfileiramento direto, validação de linha CSV |
| **Interfaces** | Endpoints REST |
| **Histórias** | US-01, US-03, US-04, US-05, US-06 |

---

## Mapa componente → histórias

| História | Domain | Application | Infrastructure | Presentation |
|---|---|---|---|---|
| US-01 | portas | IngerirClientes | Celery + arquivo + repo | POST /lotes |
| US-02 | Lote/status | Validadores | Task Celery + repo | — |
| US-03 | porta repo | ObterLote | LoteRepositorio | GET /lotes/{id} |
| US-04 | porta repo | ListarLotes | LoteRepositorio | GET /lotes |
| US-05 | portas | ReprocessarLote | Celery + repo | PUT /lotes/{id} |
| US-06 | porta repo | RemoverLote | LoteRepositorio | DELETE /lotes/{id} |
