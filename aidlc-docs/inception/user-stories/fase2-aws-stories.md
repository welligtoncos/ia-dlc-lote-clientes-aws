# Histórias de Usuário — Fase 2 Migração AWS

**Organização**: por funcionalidade (Q1=A)  
**Granularidade**: média — ~8 histórias (Q2=B)  
**AC**: Gherkin nos fluxos + bullets em ops/infra (Q3=C)  
**Personas**: P1–P4 reuso + P5 DevOps (Q4=A)  
**Arquivos Fase 1**: intactos; esta doc só deltas AWS (Q5=A)  
**Prioridade**: MoSCoW (Q6=A)  
**CM leve**: história dedicada (Q7=A)  
**Segurança**: história dedicada (Q8=A)

**Referência MVP**: `stories.md` (US-01..06) — comportamento funcional preservado (RF-AWS-13).

---

## Resumo MoSCoW

| ID | Título | Prioridade | Personas | RF / RNF |
|---|---|---|---|---|
| US-AWS-01 | Chamar a API via Gateway com API Key | Must | P1 | RF-AWS-02,03,12; RNF-AWS-04,12 |
| US-AWS-02 | Persistir CSV em S3 e enfileirar com bucket/chave | Must | P1 | RF-AWS-06,07,08 |
| US-AWS-03 | Processar lote na cloud lendo S3 (worker ECS) | Must | P4 | RF-AWS-04,05,07,09 |
| US-AWS-04 | Manter Compose local com filesystem | Must | P1 | RF-AWS-08; critério aceite 5 |
| US-AWS-05 | Provisionar stack Terraform em `dev` via GHA | Must | P5 | RF-AWS-01,11,12; RNF-AWS-01,02,11 |
| US-AWS-06 | Executar dump/restore MySQL local → RDS | Must | P5 | RF-AWS-10 |
| US-AWS-07 | Registrar mudança leve e nota de rollback | Must | P5 | RNF-AWS-16; CQ4=B |
| US-AWS-08 | Aplicar controles de segurança cloud | Must | P5, P1 | RF-AWS-14,15; RNF-AWS-03..05 |

*Should/Could*: nenhum neste ciclo — escopo = Must acima.

---

## US-AWS-01 — Chamar a API via Gateway com API Key

**Como** Integrador,  
**quero** autenticar com API Key e usar a URL do API Gateway,  
**para** enviar e consultar lotes na cloud sem expor o ALB/ECS diretamente.

**Prioridade**: Must  
**Personas**: P1  
**Mapeamento**: RF-AWS-02, RF-AWS-03, RF-AWS-12 · RNF-AWS-04, RNF-AWS-12

### Critérios de aceitação (Gherkin)

```gherkin
Given uma API Key válida configurada no API Gateway
  And a stack dev implantada em us-east-1
When o Integrador envia POST /lotes com o header de API Key e um CSV válido (<= 5 MB)
Then a resposta é 202 Accepted
  And o corpo contém lote_id e status PENDENTE (contrato MVP)
```

```gherkin
Given uma requisição sem API Key ou com key inválida
When o Integrador chama qualquer rota protegida do Gateway
Then a resposta é 401 ou 403
  And nenhum lote é criado
```

### Critérios adicionais (bullets)
- [ ] GET `/lotes` e GET `/lotes/{id}` exigem a mesma API Key (salvo health liberado no design)
- [ ] Payload de upload ≥ 5 MB suportado pelo Gateway (RNF-AWS-12)
- [ ] Smoke pós-deploy documenta URL do Gateway + uso da key

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-02 — Persistir CSV em S3 e enfileirar com bucket/chave

**Como** Integrador,  
**quero** que o upload na cloud grave o arquivo no S3 e enfileire a task com referência ao objeto,  
**para** o worker processar sem volume compartilhado.

**Prioridade**: Must  
**Personas**: P1  
**Mapeamento**: RF-AWS-06, RF-AWS-07, RF-AWS-08

### Critérios de aceitação (Gherkin)

```gherkin
Given STORAGE_BACKEND=s3 e bucket configurado
When o Integrador envia POST /lotes com CSV válido via Gateway
Then o objeto é criado sob o prefixo lotes/
  And a task ingerir_clientes é enfileirada com kwargs {lote_id, bucket, chave}
  And o status inicial do lote é PENDENTE
```

```gherkin
Given falha ao gravar no S3 (permissão ou bucket inexistente)
When o Integrador envia POST /lotes
Then a API retorna erro 5xx/4xx apropriado
  And nenhum lote fica inconsistente sem registro de falha claro
```

### Critérios adicionais (bullets)
- [ ] Nome da task permanece `ingerir_clientes`
- [ ] Adapter filesystem permanece disponível quando `STORAGE_BACKEND` ≠ `s3` (ver US-AWS-04)
- [ ] Objeto S3 verificável após upload bem-sucedido (critério aceite 4)

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-03 — Processar lote na cloud lendo S3 (worker ECS)

**Como** Worker,  
**quero** consumir a task com `{lote_id, bucket, chave}`, baixar/ler o CSV do S3 e atualizar o RDS,  
**para** concluir o lote em CONCLUIDO ou ERRO na cloud.

**Prioridade**: Must  
**Personas**: P4  
**Mapeamento**: RF-AWS-04, RF-AWS-05, RF-AWS-07, RF-AWS-09

### Critérios de aceitação (Gherkin)

```gherkin
Given um lote PENDENTE com objeto CSV válido no S3
  And o worker ECS conectado ao ElastiCache e RDS
When a task ingerir_clientes é consumida
Then o status passa por PROCESSANDO
  And ao final o lote fica CONCLUIDO ou ERRO conforme regras MVP
  And o resumo (válidos/inválidos) é persistido no RDS
```

```gherkin
Given kwargs com chave inexistente no bucket
When o worker processa a task
Then o lote termina em ERRO (ou retry esgotado conforme política existente)
  And o erro é observável nos logs CloudWatch
```

### Critérios adicionais (bullets)
- [ ] Retry Celery 3× (60/120/240) mantido (RNF-AWS-07)
- [ ] Task role com least-privilege S3 (RF-AWS-15)
- [ ] Schema `migrations/001_lotes.sql` aplicado no RDS

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-04 — Manter Compose local com filesystem

**Como** Integrador / desenvolvedor,  
**quero** continuar subindo o stack local com storage em filesystem,  
**para** desenvolver e smoke-testar sem AWS.

**Prioridade**: Must  
**Personas**: P1  
**Mapeamento**: RF-AWS-08 · critério aceite 5

### Critérios de aceitação (Gherkin)

```gherkin
Given Docker Compose local e STORAGE_BACKEND=fs (ou default local)
When executo o smoke local (POST /lotes + worker + GET)
Then o fluxo completa sem depender de S3/API Gateway
  And o arquivo permanece no volume compartilhado
```

### Critérios adicionais (bullets)
- [ ] Documentação deixa claro quando usar `fs` vs `s3`
- [ ] Testes unitários/PBT do adapter local continuam verdes

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-05 — Provisionar stack Terraform em `dev` via GHA

**Como** DevOps,  
**quero** que o pipeline build/push ECR e `terraform apply` no ambiente **dev**,  
**para** ter a stack (RDS, APIGW, ALB, ECS, S3, ElastiCache) reproduzível em `us-east-1`.

**Prioridade**: Must  
**Personas**: P5  
**Mapeamento**: RF-AWS-01, RF-AWS-11, RF-AWS-12 · RNF-AWS-01, RNF-AWS-02, RNF-AWS-11

### Critérios de aceitação (Gherkin)

```gherkin
Given credenciais/OIDC de CI configurados para a conta AWS de dev
When um merge/workflow elegível dispara o GitHub Actions
Then as imagens api e worker são publicadas no ECR
  And terraform apply conclui sem erro no ambiente dev
```

```gherkin
Given a stack aplicada
When executo o smoke cloud (health + POST + GET via Gateway)
Then o fluxo assíncrono completa (CONCLUIDO ou ERRO legítimo)
```

### Critérios adicionais (bullets)
- [ ] Single-AZ; RDS `db.t4g.micro` (ou equivalente)
- [ ] Apply automático **somente** em `dev` (sem prod neste ciclo)
- [ ] Outputs Terraform incluem URL do Gateway / nomes de recursos necessários ao smoke

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-06 — Executar dump/restore MySQL local → RDS

**Como** DevOps,  
**quero** um procedimento documentado de dump/restore do MySQL local para o RDS,  
**para** opcionalmente levar dados de desenvolvimento local para a cloud.

**Prioridade**: Must  
**Personas**: P5  
**Mapeamento**: RF-AWS-10

### Critérios de aceitação (Gherkin)

```gherkin
Given um MySQL local com schema de lotes e um RDS acessível (bastion/VPN/SG conforme design)
When sigo o procedimento documentado de dump e restore
Then o schema (e dados escolhidos) ficam disponíveis no RDS
  Or um dry-run documentado prova os passos sem carga real
```

### Critérios adicionais (bullets)
- [ ] Artefato em `docs/` ou `infra/` com pré-requisitos e riscos
- [ ] Procedimento não exige secrets no repositório

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-07 — Registrar mudança leve e nota de rollback

**Como** DevOps,  
**quero** que cada mudança em `dev` deixe trilha no PR/GHA e uma nota de rollback,  
**para** cumprir o change management leve (CQ4=B / RNF-AWS-16).

**Prioridade**: Must  
**Personas**: P5  
**Mapeamento**: RNF-AWS-16 · RESILIENCY-03

### Critérios de aceitação (bullets)
- [ ] PR (ou run do GHA) serve como registro da mudança aplicada em `dev`
- [ ] README ou runbook contém nota de rollback (ex.: redeploy tag anterior / `terraform apply` de revisão anterior)
- [ ] Isenção de CAB formal documentada (ambiente Low / só `dev`)

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## US-AWS-08 — Aplicar controles de segurança cloud

**Como** DevOps (e Integrador indiretamente),  
**quero** API Key, S3 privado, secrets gerenciados e IAM least-privilege,  
**para** atender o Security Baseline no ambiente `dev`.

**Prioridade**: Must  
**Personas**: P5, P1  
**Mapeamento**: RF-AWS-14, RF-AWS-15 · RNF-AWS-03, RNF-AWS-04, RNF-AWS-05

### Critérios de aceitação (Gherkin)

```gherkin
Given a stack Terraform aplicada
When inspeciono o bucket S3 de lotes
Then o bucket não é público
  And o acesso da aplicação usa task role (não credenciais no código)
```

```gherkin
Given secrets de DB/broker/API Key
When a aplicação sobe no ECS
Then os valores vêm de Secrets Manager ou SSM
  And não há secrets commitados no repositório
```

### Critérios adicionais (bullets)
- [ ] RDS sem IP público; SGs restritivos
- [ ] TLS no ALB/Gateway
- [ ] Criptografia em repouso defaults RDS/S3
- [ ] Revisão de policies IAM registrada no aceite

### INVEST
Independent · Negotiable · Valuable · Estimable · Small · Testable

---

## Mapa História → Persona

| História | Personas |
|---|---|
| US-AWS-01 | P1 |
| US-AWS-02 | P1 |
| US-AWS-03 | P4 |
| US-AWS-04 | P1 |
| US-AWS-05 | P5 |
| US-AWS-06 | P5 |
| US-AWS-07 | P5 |
| US-AWS-08 | P5, P1 |
