# Requisitos — Serviço de Ingestão de Clientes

**Versão**: 1.0  
**Data**: 2026-08-12  
**Status**: Aprovado  
**Fonte**: PRD v1.0 + respostas em `requirement-verification-questions.md`

---

## 1. Análise de Intenção

| Campo | Valor |
|---|---|
| **Solicitação do usuário** | Gerar Inception AI-DLC a partir do PRD de ingestão de clientes |
| **Tipo** | Novo projeto (greenfield) |
| **Escopo** | Múltiplos componentes (API, worker, broker, banco, Docker) |
| **Complexidade** | Moderada–Complexa |
| **Profundidade** | Abrangente |
| **Entrega deste ciclo** | Fase 1 — MVP local apenas (`docker-compose`) |

---

## 2. Visão e Objetivos

### Visão
Serviço que recebe CSV de cadastros de clientes, valida cada registro de forma assíncrona e disponibiliza resumo de qualidade (total, válidas, inválidas), com rastreabilidade do lote.

### Objetivos (este ciclo)
- Aceitar upload CSV e processar em background (fire-and-forget).
- Validar linhas conforme regras de qualidade.
- Persistir status e resumo do lote de forma durável e consultável.
- Expor CRUD de lotes via API.
- Rodar de forma idêntica em local via Docker Compose (mesmo artefato preparado para AWS futura, sem implementar AWS neste ciclo).

### Não-objetivos
- Persistir cada cliente individualmente (só resumo agregado).
- Autenticação/autorização de usuários.
- Interface gráfica.
- Correção/normalização automática de dados inválidos.
- Orquestração de workflows multi-task.
- Provisionamento/deploy AWS (Fase 2 — fora deste ciclo).

---

## 3. Personas e Casos de Uso

| Persona | Necessidade |
|---|---|
| Sistema integrador / script | Enviar lotes e acompanhar por API |
| Analista de dados | Consultar status e resumo de qualidade |
| Operador | Reprocessar lotes em `ERRO`; remover ingestões |

| ID | Caso de uso |
|---|---|
| UC-01 | Enviar `clientes.csv` e receber `task_id` imediatamente |
| UC-02 | Consultar lote e ver status + resumo |
| UC-03 | Listar todas as ingestões |
| UC-04 | Reprocessar lote em `ERRO` |
| UC-05 | Remover registro de uma ingestão |

---

## 4. Requisitos Funcionais

| ID | Requisito | Origem |
|---|---|---|
| RF-01 | Aceitar upload CSV via `POST /lotes` | PRD |
| RF-02 | Criar lote `PENDENTE`, responder `202 Accepted` com `lote_id`, `task_id` e `status`, sem processar de forma síncrona | PRD |
| RF-03 | Worker consome a tarefa, lê o CSV e valida cada linha (seção 6) | PRD |
| RF-04 | Ao concluir, atualizar `total_linhas`, `linhas_validas`, `linhas_invalidas` e status `CONCLUIDO` | PRD |
| RF-05 | Em falha (após retries esgotados), status `ERRO` + mensagem | PRD + Q5 |
| RF-06 | `GET /lotes/{id}` retorna status e resumo | PRD |
| RF-07 | `GET /lotes` lista todas as ingestões | PRD |
| RF-08 | `PUT /lotes/{id}` reprocessa **apenas** lotes em `ERRO` | PRD + Q7 |
| RF-09 | `DELETE /lotes/{id}` remove o registro no MySQL; **arquivo CSV permanece** no volume | PRD + Q8 |
| RF-10 | Nome da tarefa validado contra allowlist (`TAREFAS_SUPORTADAS`) antes do enfileiramento | PRD |
| RF-11 | CSV: cabeçalho obrigatório `nome,email,cpf,telefone`; separador `,`; encoding UTF-8 | Q2 |
| RF-12 | Rejeitar upload com tamanho > 5 MB (HTTP 413 ou 400 com mensagem clara) | Q3 |
| RF-13 | Arquivo salvo em volume/disco compartilhado entre api e worker; task recebe caminho, não o conteúdo | Q4 |
| RF-14 | Ciclo de status: `PENDENTE → PROCESSANDO → CONCLUIDO` ou `ERRO` | PRD |
| RF-15 | Idempotência: usar `celery_task_id` / chave de idempotência para não reexecutar task já concluída com sucesso | Q6 |
| RF-16 | Mitigar ambiguidade Celery `PENDING`: status canônico do lote vive no MySQL | PRD |

---

## 5. Requisitos Não Funcionais

| ID | Categoria | Requisito |
|---|---|---|
| RNF-01 | Desempenho | `POST /lotes` responde em centenas de ms, independente do tamanho (até 5 MB) |
| RNF-02 | Escalabilidade | API e worker escalam de forma independente (preparação arquitetural; no MVP, um de cada no compose) |
| RNF-03 | Confiabilidade | Retry Celery: até 3 tentativas, backoff exponencial (60s, 120s, 240s); depois `ERRO` |
| RNF-04 | Idempotência | Ver RF-15 |
| RNF-05 | Segurança (MVP) | Credenciais via variáveis de ambiente; sem secrets no código. Auth de API fora de escopo |
| RNF-06 | Observabilidade | Logs estruturados de API e worker (stdout; coletáveis no compose) |
| RNF-07 | Portabilidade | Imagem Docker única (api/worker por comando); local via compose; AWS futura sem mudar código |
| RNF-08 | Durabilidade | Status/resumo no MySQL (não depender do result backend do Celery/Valkey) |
| RNF-09 | Idioma | Artefatos AI-DLC, código, comentários e API em português |
| RNF-10 | Testes PBT | Extensão Property-Based Testing **habilitada** (modo completo) — propriedades de validação (CPF, e-mail, telefone, contagens) devem ser identificadas no design e cobertas na Construction |

---

## 6. Regras de Validação de Linha

Uma linha é **válida** se atender a todas; caso contrário conta em `linhas_invalidas`.

| Campo | Regra |
|---|---|
| `nome` | Obrigatório; não vazio (após trim) |
| `email` | Obrigatório; formato `usuario@dominio.tld` |
| `cpf` | Obrigatório; 11 dígitos + dígito verificador válido |
| `telefone` | Opcional; se presente, apenas dígitos e entre **10 e 11** dígitos |

Sem correção/normalização automática nesta versão.

---

## 7. Contrato da API

| Método | Rota | Descrição | Fila? |
|---|---|---|---|
| POST | `/lotes` | Upload CSV → lote `PENDENTE` → enfileira → `202` | Sim |
| GET | `/lotes` | Lista ingestões | Não |
| GET | `/lotes/{id}` | Status e resumo | Não |
| PUT | `/lotes/{id}` | Reprocessa se `ERRO` | Sim |
| DELETE | `/lotes/{id}` | Remove registro MySQL | Não |

**POST 202 — exemplo:**
```json
{ "lote_id": 42, "task_id": "a1b2c3...", "status": "PENDENTE" }
```

**GET — exemplo:**
```json
{
  "lote_id": 42,
  "nome_arquivo": "clientes.csv",
  "status": "CONCLUIDO",
  "total_linhas": 1000,
  "linhas_validas": 947,
  "linhas_invalidas": 53
}
```

---

## 8. Modelo de Dados

```sql
CREATE TABLE lotes (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo     VARCHAR(255) NOT NULL,
    status           VARCHAR(20)  NOT NULL DEFAULT 'PENDENTE',
    total_linhas     INT          DEFAULT 0,
    linhas_validas   INT          DEFAULT 0,
    linhas_invalidas INT          DEFAULT 0,
    erro             TEXT,
    celery_task_id   VARCHAR(155),
    criado_em        DATETIME DEFAULT CURRENT_TIMESTAMP,
    concluido_em     DATETIME NULL
) ENGINE=InnoDB;
```

---

## 9. Arquitetura e Stack (diretrizes)

| Camada | Tecnologia |
|---|---|
| Estilo | Hexagonal (ports & adapters); domínio depende de `PortaTarefa` |
| API | FastAPI + Uvicorn |
| Fila | Celery |
| Broker/backend | Valkey (`redis://`) |
| Banco | MySQL 8 |
| ORM | SQLAlchemy + PyMySQL |
| Parsing | pandas ou `csv` nativo |
| Empacotamento | Docker + Docker Compose (api, worker, valkey, mysql) |

Fluxo: `Presentation → Application → Domain (PortaTarefa) → Infrastructure (AdaptadorCelery → task → repositório)`

Armazenamento de arquivo (MVP): volume compartilhado entre api e worker.

---

## 10. Critérios de Aceitação / Sucesso

- `POST /lotes` em menos de algumas centenas de ms para arquivos ≤ 5 MB.
- 100% dos lotes terminam em `CONCLUIDO` ou `ERRO` consultáveis (sem lotes “presos” após retries).
- Contagens refletem corretamente CSVs de qualidade conhecida (incl. casos PBT).
- CRUD completo funcional via compose.
- Cabeçalho/separador/encoding inválidos rejeitados ou classificados de forma documentada.

---

## 11. Decisões Capturadas nas Perguntas

| # | Decisão |
|---|---|
| Q1 | Escopo = Fase 1 MVP local |
| Q2 | CSV: `nome,email,cpf,telefone` / `,` / UTF-8 |
| Q3 | Limite 5 MB |
| Q4 | Volume compartilhado |
| Q5 | Retry 3× com backoff 60/120/240s |
| Q6 | Idempotência via `celery_task_id` |
| Q7 | Reprocessar só `ERRO` |
| Q8 | DELETE só banco; arquivo permanece |
| Q9 | Telefone 10–11 dígitos |
| Q10 | Português em artefatos e código |
| Q11 | Security Baseline: **desabilitado** |
| Q12 | Resiliency Baseline: **desabilitado** |
| Q13 | PBT: **habilitado (completo)** |

---

## 12. Extensões

| Extensão | Status | Implicação |
|---|---|---|
| Security Baseline | Não | Regras SECURITY não bloqueantes |
| Resiliency Baseline | Não | Baseline de resiliência não aplicado |
| Property-Based Testing | Sim (completo) | PBT-01..PBT aplicáveis nas fases de design/código; validadores e invariantes de contagem são candidatos naturais |

---

## 13. Riscos Residuais

- Result backend Valkey é efêmero — mitigado por MySQL.
- Serialização: apenas IDs/caminhos na mensagem da task.
- DELETE não limpa disco — possível acúmulo de arquivos no volume (aceitável no MVP; documentar).
- AWS fora de escopo — portabilidade preservada via env vars e imagem única.
