# Design da Aplicação — Consolidado

**Projeto**: Serviço de Ingestão de Clientes (MVP local)  
**Estilo**: Hexagonal (ports & adapters)  
**Idioma**: Português nos identificadores

## Decisões do plano

| # | Escolha | Decisão |
|---|---|---|
| Q1 | A | 4 componentes: Domain, Application, Infrastructure, Presentation |
| Q2 | B | Validação de linha na **Application** (funções puras para PBT) |
| Q3 | A | `PortaLoteRepositorio` no Domain |
| Q4 | A | Um caso de uso por operação de API |
| Q5 | A | `PortaArmazenamentoArquivo` + adapter local |
| Q6 | A | Métodos com assinaturas e propósito curto |

## Estrutura-alvo (código)

> **Atualizado na Units Generation**: projetos Python segregados (`lote-api`, `lote-worker`, `lote-shared`). A árvore hexagonal abaixo descreve o **modelo lógico**; o layout físico está em `unit-of-work.md`.

**Físico (obrigatório):**
```text
libs/   → lote-shared   (domain, portas, validacao, persistence)
api/    → lote-api      (presentation, application, adapters HTTP/enqueue)
worker/ → lote-worker   (celery_app, tasks, adapters do worker)
```

**Lógico (hexagonal — distribuído entre os projetos):**
```text
lote_shared/
├── domain/          # Lote, PortaTarefa, PortaLoteRepositorio, PortaArmazenamentoArquivo
├── validacao/       # validadores_cliente (PBT)
└── persistence/     # LoteRepositorio

lote_api/
├── presentation/routes/lotes.py
├── application/casos_uso/...
└── infrastructure/adapters/...

lote_worker/
├── celery_app.py
└── tasks/ingerir_clientes.py
```

## Artefatos deste estágio

| Arquivo | Conteúdo |
|---|---|
| [components.md](./components.md) | Responsabilidades C1–C4 |
| [component-methods.md](./component-methods.md) | Assinaturas e portas |
| [services.md](./services.md) | Orquestração dos casos de uso |
| [component-dependency.md](./component-dependency.md) | Matriz e fluxos |

## Portas do domínio

1. **PortaTarefa** — enfileirar / consultar task  
2. **PortaLoteRepositorio** — CRUD de `Lote`  
3. **PortaArmazenamentoArquivo** — salvar/verificar CSV no volume  

## Cobertura de histórias

US-01..US-06 mapeadas em components.md; worker cobre US-02 via task + validadores.

## Extensões

| Extensão | Status | Nota |
|---|---|---|
| Security | Off | N/A |
| Resiliency | Off | N/A |
| PBT | On | Foco em `validadores_cliente` e `resumir_validacao` (Functional Design detalhará propriedades) |

## Próximo estágio

**Units Generation** — decompor em unidades de trabalho (hipótese: dominio-api + worker-validacao).
