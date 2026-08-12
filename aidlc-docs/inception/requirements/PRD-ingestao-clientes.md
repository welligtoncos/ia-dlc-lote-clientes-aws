# PRD — Serviço de Ingestão de Clientes

| | |
|---|---|
| **Versão** | 1.0 |
| **Data** | 11/08/2026 |
| **Status** | Rascunho para implementação |
| **Autor** | _(seu nome)_ |
| **Stack** | FastAPI · Celery · Valkey · MySQL |

---

## 1. Visão geral

Serviço que recebe arquivos CSV com cadastros de clientes, valida cada registro em segundo plano e disponibiliza um resumo de qualidade dos dados (linhas totais, válidas e inválidas). O processamento é **assíncrono**: a API aceita o arquivo, responde imediatamente e devolve um identificador que o cliente usa para consultar o andamento.

O projeto demonstra, em escopo pequeno, um padrão de ingestão de dados realista — com rastreabilidade, validação e processamento desacoplado — construído sobre arquitetura hexagonal e o padrão assíncrono _fire-and-forget_.

---

## 2. Contexto e problema

Empresas recebem cadastros de clientes em lote (de parceiros, formulários exportados, sistemas legados). Esses arquivos chegam grandes e com qualidade irregular: campos faltando, e-mails malformados, CPFs inválidos.

Dois problemas precisam ser resolvidos ao mesmo tempo:

1. **Não travar o solicitante.** Validar milhares de linhas leva tempo; fazer isso de forma síncrona deixaria a requisição pendurada e esbarraria em _timeouts_ (por exemplo, o limite de 29s do API Gateway).
2. **Saber a procedência e a qualidade.** É preciso registrar de qual arquivo cada ingestão veio, quando ocorreu e quantos registros passaram na validação — informação essencial de engenharia de dados.

Este serviço ataca os dois: processa em background e mantém uma tabela de controle com o ciclo de vida e as métricas de cada ingestão.

---

## 3. Objetivos e não-objetivos

### Objetivos

- Aceitar um CSV de clientes e processá-lo de forma assíncrona.
- Validar cada linha segundo regras de qualidade definidas (seção 12).
- Registrar o status e o resumo de cada ingestão de forma durável e consultável.
- Expor um CRUD sobre as ingestões (lotes).
- Rodar de forma idêntica em ambiente local e na AWS, sem alterar código.

### Não-objetivos (fora de escopo nesta versão)

- Persistir cada registro de cliente individualmente (apenas o resumo agregado é gravado).
- Autenticação/autorização de usuários da API.
- Interface gráfica (o consumo é via API).
- Correção ou normalização automática de dados inválidos (apenas classificação).
- Orquestração de múltiplas tarefas encadeadas (_workflows_).

---

## 4. Público-alvo

| Persona | Necessidade |
|---|---|
| Sistema integrador / script | Enviar lotes de clientes e acompanhar o processamento por API. |
| Analista de dados | Consultar quantos registros de um lote foram válidos e quantos falharam. |
| Operador | Reprocessar um lote que falhou; remover ingestões antigas. |

---

## 5. Casos de uso

- **UC-01** — Como integrador, envio um `clientes.csv` e recebo na hora um `task_id` para acompanhar.
- **UC-02** — Como analista, consulto um lote e vejo o status e o resumo (total, válidas, inválidas).
- **UC-03** — Como analista, listo todas as ingestões já realizadas.
- **UC-04** — Como operador, reprocesso um lote que terminou com erro.
- **UC-05** — Como operador, removo o registro de uma ingestão.

---

## 6. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF-01 | O sistema deve aceitar upload de um arquivo CSV via `POST /lotes`. |
| RF-02 | Ao receber o arquivo, o sistema deve criar um lote com status `PENDENTE` e responder `202 Accepted` com o `task_id`, sem processar o arquivo de forma síncrona. |
| RF-03 | Um worker deve consumir a tarefa, ler o CSV e validar cada linha segundo as regras da seção 12. |
| RF-04 | Ao concluir, o worker deve atualizar o lote com `total_linhas`, `linhas_validas`, `linhas_invalidas` e status `CONCLUIDO`. |
| RF-05 | Em caso de falha no processamento, o lote deve receber status `ERRO` e a mensagem correspondente. |
| RF-06 | O sistema deve permitir consultar um lote por ID (`GET /lotes/{id}`), retornando status e resumo. |
| RF-07 | O sistema deve permitir listar todos os lotes (`GET /lotes`). |
| RF-08 | O sistema deve permitir reprocessar um lote em `ERRO` (`PUT /lotes/{id}`). |
| RF-09 | O sistema deve permitir remover um lote (`DELETE /lotes/{id}`). |
| RF-10 | O nome da tarefa disparada deve ser validado contra uma lista de tarefas permitidas (_allowlist_) antes do enfileiramento. |

---

## 7. Requisitos não-funcionais

| ID | Categoria | Requisito |
|---|---|---|
| RNF-01 | Desempenho | A resposta do `POST /lotes` deve ocorrer em milissegundos, independente do tamanho do arquivo. |
| RNF-02 | Escalabilidade | API e worker devem escalar de forma independente (a API por volume de requisições, o worker por tamanho da fila). |
| RNF-03 | Confiabilidade | Tarefas que falharem devem poder ser retentadas automaticamente (_retry_ com limite). |
| RNF-04 | Idempotência | O reenvio da mesma tarefa não deve duplicar o processamento. |
| RNF-05 | Segurança | Credenciais de banco e broker não devem estar no código; devem vir de variáveis de ambiente (Secrets Manager em produção). |
| RNF-06 | Observabilidade | Logs de API e worker devem ser coletados de forma centralizada. |
| RNF-07 | Portabilidade | O mesmo artefato (imagem Docker) deve rodar em ambiente local e na AWS, mudando apenas variáveis de ambiente. |
| RNF-08 | Durabilidade | O status e o resumo dos lotes devem sobreviver a reinícios (persistidos em banco relacional, não apenas no backend efêmero do Celery). |

---

## 8. Arquitetura técnica

### Estilo arquitetural

Arquitetura **hexagonal** (ports & adapters). A lógica de aplicação depende de uma interface de domínio (`PortaTarefa`), e não do Celery diretamente. O `AdaptadorCelery`, na infraestrutura, implementa essa interface. Isso mantém o Celery como um detalhe substituível.

**Fluxo pelas camadas:**
`Presentation (rotas) → Application (caso de uso) → Domain (PortaTarefa) → Infrastructure (AdaptadorCelery → task → repositório)`

### Stack de tecnologias

| Camada | Tecnologia | Papel |
|---|---|---|
| API | FastAPI + Uvicorn | Endpoints HTTP e documentação automática. |
| Fila | Celery | Sistema de tarefas assíncronas. |
| Broker / backend | Valkey _(via ElastiCache em produção)_ | Transporte das mensagens e resultado das tasks. Conexão via protocolo Redis (`redis://`). |
| Banco | MySQL 8 _(via RDS em produção)_ | Tabela de controle `lotes` (dado durável). |
| ORM / driver | SQLAlchemy + PyMySQL | Acesso ao banco. |
| Parsing | pandas _(ou `csv` nativo)_ | Leitura e validação do CSV. |
| Empacotamento | Docker + Docker Compose | Imagem única (API e worker) e ambiente local. |

### Estrutura de pastas

```
app/
├── domain/
│   ├── ports/porta_tarefa.py            # interface: executar, obter_status
│   └── models/lote.py                   # entidade Lote
├── application/
│   └── casos_uso/ingerir_clientes.py    # valida entrada + enfileira via porta
├── infrastructure/
│   ├── celery_app.py                    # broker/backend Valkey
│   ├── adapters/adaptador_celery.py     # implementa PortaTarefa + TAREFAS_SUPORTADAS
│   ├── tasks/ingerir_clientes.py        # @shared_task: lê CSV, valida, grava resumo
│   └── repositories/lote_repo.py        # acesso ao MySQL
└── presentation/
    └── routes/lotes.py                  # endpoints do CRUD
```

---

## 9. Modelo de dados

Tabela única `lotes` (tabela de controle das ingestões):

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

**Ciclo de status:** `PENDENTE → PROCESSANDO → CONCLUIDO` ou `ERRO`.

---

## 10. Contrato da API

| Método | Rota | Descrição | Fila? |
|---|---|---|---|
| POST | `/lotes` | Recebe o CSV, cria o lote `PENDENTE`, enfileira e responde `202` + `task_id`. | Sim |
| GET | `/lotes` | Lista todas as ingestões. | Não |
| GET | `/lotes/{id}` | Retorna status e resumo de um lote. | Não |
| PUT | `/lotes/{id}` | Reprocessa um lote em `ERRO`. | Sim |
| DELETE | `/lotes/{id}` | Remove o registro da ingestão. | Não |

**Exemplo de resposta do `POST /lotes` (`202 Accepted`):**

```json
{ "lote_id": 42, "task_id": "a1b2c3...", "status": "PENDENTE" }
```

**Exemplo de resposta do `GET /lotes/42`:**

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

## 11. Fluxo assíncrono (fire-and-forget)

1. Cliente envia `clientes.csv` no `POST /lotes`.
2. A camada de apresentação chama o `CasoUsoIngerirClientes`.
3. O caso de uso valida o mínimo (arquivo presente, extensão `.csv`), cria o lote `PENDENTE` no banco e chama `PortaTarefa.executar("ingerir_clientes", {lote_id, caminho})`.
4. O `AdaptadorCelery` confere o _allowlist_ (`TAREFAS_SUPORTADAS`), enfileira via `apply_async` e retorna o `task_id`.
5. A API responde `202 Accepted`.
6. O worker (já em execução) consome a mensagem, busca o lote, lê o CSV, valida cada linha, conta válidas/inválidas e grava o resumo (`CONCLUIDO`).
7. O cliente consulta `GET /lotes/{id}` e obtém o resultado.

---

## 12. Regras de validação

Uma linha é considerada **válida** se atender a todas as regras abaixo; caso contrário, é contabilizada em `linhas_invalidas`.

| Campo | Regra |
|---|---|
| `nome` | Obrigatório; não pode ser vazio. |
| `email` | Obrigatório; deve ter formato válido (`usuario@dominio.tld`). |
| `cpf` | Obrigatório; deve ter 11 dígitos e dígito verificador válido. |
| `telefone` | Opcional; se presente, deve conter apenas dígitos em quantidade plausível. |

> Nesta versão o sistema apenas **classifica** as linhas; não corrige nem normaliza os dados inválidos.

---

## 13. Infraestrutura

### Local (ambiente de desenvolvimento)

Quatro containers via `docker-compose`: **api**, **worker** (mesma imagem, comandos diferentes), **valkey** e **mysql**. Conexões definidas por variáveis de ambiente no próprio compose.

### AWS (produção)

Mapeamento direto do ambiente local, sem alteração de código:

| Local | AWS |
|---|---|
| container api/worker | 2 serviços no **ECS Fargate** (mesma imagem) |
| imagem Docker | **ECR** |
| valkey | **ElastiCache (Valkey)** |
| mysql | **RDS MySQL** |
| variáveis do compose | **Secrets Manager** |
| — | **ALB** (porta de entrada) |
| — | **IAM** (Task Roles) e **CloudWatch** (logs) |

> O API Gateway é opcional e não faz parte do escopo mínimo; entraria à frente do ALB (via VPC Link) apenas se fossem necessários _rate limiting_, API keys ou autenticação gerenciada.

---

## 14. Métricas de sucesso

- Tempo de resposta do `POST /lotes` inferior a algumas centenas de milissegundos, independente do tamanho do arquivo.
- 100% dos lotes terminam com status final consultável (`CONCLUIDO` ou `ERRO`), sem lotes "presos".
- As contagens de linhas válidas/inválidas refletem corretamente o conteúdo do arquivo em testes com CSVs de qualidade conhecida.
- O mesmo artefato roda local e na AWS sem alteração de código.

---

## 15. Roadmap

| Fase | Entrega |
|---|---|
| **1 — MVP local** | CRUD completo, worker validando o CSV, tudo rodando via `docker-compose`. |
| **2 — Deploy AWS** | Provisionar a infraestrutura (preferencialmente via Terraform ou AWS Copilot) e publicar o serviço. |
| **3 — Persistência granular** | Reintroduzir a tabela `registros` (com FK para `lotes`) para guardar cada cliente individualmente. |
| **4 — Extras** | API Gateway com _rate limiting_, agendamento periódico (Celery Beat), ingestão a partir de arquivos no S3. |

---

## 16. Riscos e questões em aberto

- **Ambiguidade do status `PENDING` do Celery.** O Celery retorna `PENDING` tanto para tarefas na fila quanto para IDs inexistentes. Mitigação: registrar a criação da tarefa no próprio lote e distinguir os casos na consulta de status.
- **Result backend efêmero.** Resultados no Valkey expiram; por isso o dado durável fica no MySQL, não no backend do Celery.
- **Serialização de argumentos.** Apenas dados simples (IDs, valores) devem ser passados para a task; o arquivo é referenciado por caminho, e o worker busca o dado atualizado.
- **Definição do formato do CSV.** Cabeçalho, separador e codificação esperados precisam ser fixados e documentados.

---

## 17. Evolução futura

O desenho já contempla, sem retrabalho estrutural: persistência granular por registro, entrada via S3 em vez de upload direto, agregações analíticas (por exemplo, via Athena) antes de gravar o resumo, e agendamento de ingestões recorrentes. Como a lógica vive atrás da `PortaTarefa`, o domínio é intercambiável — o mesmo esqueleto suporta outros tipos de ingestão sem alterar as camadas de aplicação e apresentação.
