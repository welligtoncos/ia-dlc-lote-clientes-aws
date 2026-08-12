# Perguntas de Verificação de Requisitos

Responda cada pergunta preenchendo a letra após a tag `[Answer]:`.
Se nenhuma opção servir, use a última opção (Other / Outro) e descreva.

Quando terminar, avise no chat (ex.: "pronto" / "respondi as perguntas").

---

## Question 1
Qual é o **escopo desta entrega** que o Inception/Construction deve cobrir agora?

A) Apenas Fase 1 — MVP local (`docker-compose`: api, worker, valkey, mysql) com CRUD + validação CSV

B) Fase 1 + desenho/provisionamento AWS (Fase 2: ECS, ECR, ElastiCache, RDS, ALB, Secrets Manager) no mesmo ciclo

C) Fase 1 completa + apenas documentação/IaC esboçada da AWS (sem deploy real neste ciclo)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 2
Qual o **formato esperado do CSV** de entrada?

A) Cabeçalho obrigatório `nome,email,cpf,telefone`; separador `,`; encoding UTF-8

B) Cabeçalho obrigatório `nome;email;cpf;telefone`; separador `;`; encoding UTF-8

C) Cabeçalho obrigatório `nome,email,cpf,telefone`; separador `,`; encoding UTF-8 com BOM aceito

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3
Qual o **tamanho máximo** aceito no upload do CSV?

A) Até 5 MB

B) Até 20 MB

C) Até 100 MB

D) Sem limite rígido no MVP (apenas validação de extensão `.csv`)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
Como o arquivo deve ser **armazenado entre o upload e o worker**?

A) Volume/disco compartilhado entre containers api e worker (caminho local referenciado na task)

B) Salvar o CSV em storage de objeto (S3 local/MinIO no compose; S3 real na AWS)

C) Passar o conteúdo do arquivo na mensagem da fila (apenas para arquivos pequenos; não preferido pelo PRD)

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 5
Qual a **política de retry** do Celery para tarefas que falharem?

A) Até 3 tentativas, backoff exponencial (ex.: 60s, 120s, 240s), depois status `ERRO`

B) Até 5 tentativas, intervalo fixo de 30s, depois status `ERRO`

C) Sem retry automático no MVP — falha imediata vai para `ERRO`; reprocessamento só via `PUT /lotes/{id}`

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 6
Como garantir **idempotência** no reenvio/reprocessamento da mesma tarefa?

A) Se o lote já está `PROCESSANDO` ou `CONCLUIDO`, rejeitar novo enfileiramento (409/400)

B) Usar `celery_task_id` / chave de idempotência: mesma task não é reexecutada se já concluída com sucesso

C) Reprocessar sempre sobrescreve contagens do lote (permitido apenas a partir de `ERRO`, conforme RF-08)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 7
O reprocessamento (`PUT /lotes/{id}`) deve ser permitido **apenas** para status `ERRO`?

A) Sim — apenas `ERRO` (conforme RF-08)

B) Também permitir reprocessar `CONCLUIDO` (reexecução manual)

C) Permitir qualquer status exceto `PROCESSANDO`

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 8
O que acontece no `DELETE /lotes/{id}` em relação ao arquivo CSV no disco/storage?

A) Apaga apenas o registro no MySQL; arquivo permanece

B) Apaga registro no MySQL e remove o arquivo associado

C) Soft-delete no banco (marca como removido); arquivo permanece

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 9
Para o campo `telefone` opcional, qual a regra de "quantidade plausível" de dígitos?

A) Entre 10 e 11 dígitos (Brasil: DDD + número)

B) Entre 8 e 15 dígitos (faixa internacional ampla)

C) Apenas dígitos, sem validar quantidade no MVP

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10
Qual a prioridade de **linguagem/documentação** dos artefatos AI-DLC e do código?

A) Artefatos AI-DLC em português; código/comentários/API em português

B) Artefatos AI-DLC em português; código (identificadores, OpenAPI) em inglês; mensagens de erro da API em português

C) Tudo em inglês

X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 11 — Security Extensions
As regras da extensão de segurança devem ser aplicadas neste projeto?

A) Sim — aplicar todas as regras SECURITY como restrições bloqueantes (recomendado para aplicações de nível de produção)

B) Não — pular todas as regras SECURITY (adequado para PoCs, protótipos e projetos experimentais)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 12 — Resiliency Extensions
O baseline de resiliência deve ser aplicado neste projeto?

**O que esta extensão é.** Ativá-la aplica melhores práticas direcionais de design para sistemas resilientes (AWS Well-Architected — Reliability Pillar). **Não** certifica prontidão de produção.

A) Sim — aplicar o baseline de resiliência como melhores práticas direcionais e orientação de design

B) Não — pular o baseline de resiliência (adequado para PoCs/protótipos)

X) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 13 — Property-Based Testing Extension
As regras de testes baseados em propriedades (PBT) devem ser aplicadas neste projeto?

A) Sim — aplicar todas as regras PBT como restrições bloqueantes

B) Parcial — aplicar PBT apenas para funções puras e round-trips de serialização (ex.: validação de CPF/e-mail)

C) Não — pular todas as regras PBT

X) Other (please describe after [Answer]: tag below)

[Answer]:  A
