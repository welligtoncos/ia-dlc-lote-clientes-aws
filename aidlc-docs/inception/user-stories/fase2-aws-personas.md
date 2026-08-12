# Personas — Fase 2 Migração AWS

**Base**: `fase2-aws-requirements.md` + plano aprovado (Q4=A)  
**Fase 1**: personas P1–P4 em `personas.md` permanecem válidas; esta Fase 2 **reusa** e **adiciona P5**.

---

## P1 — Integrador (sistema / script) — *reuso + delta cloud*

| Campo | Descrição |
|---|---|
| **Papel** | Sistema externo ou script que envia lotes |
| **Objetivo** | Enviar CSV via URL do **API Gateway** com **API Key** e acompanhar status |
| **Motivações** | Mesmo contrato funcional do MVP; autenticação e base URL mudam na cloud |
| **Dores** | 401/403 sem key; payload Gateway vs ALB; limite 5 MB |
| **Comportamento** | Header `x-api-key` (ou equivalente); `POST/GET /lotes` na URL do Gateway |
| **Histórias Fase 2** | US-AWS-01, US-AWS-02, US-AWS-04 |

---

## P2 — Analista de dados — *reuso*

| Campo | Descrição |
|---|---|
| **Papel** | Avalia qualidade dos cadastros |
| **Objetivo** | Consultar lotes/resumo (RF MVP inalterado) via Gateway autenticado |
| **Motivações** | Mesmos `GET /lotes` / `GET /lotes/{id}` |
| **Dores** | Precisa da API Key se consumir a URL pública do Gateway |
| **Comportamento** | Consultas autenticadas na cloud |
| **Histórias Fase 2** | (delta coberto em US-AWS-01; US-03/04 Fase 1 permanecem) |

---

## P3 — Operador — *reuso*

| Campo | Descrição |
|---|---|
| **Papel** | Recupera falhas e limpa registros |
| **Objetivo** | Reprocessar `ERRO` e DELETE (comportamento MVP) na cloud |
| **Motivações** | Mesmos endpoints; dados em RDS |
| **Dores** | Distinguir falha de app vs infra |
| **Comportamento** | `PUT`/`DELETE` via Gateway + API Key |
| **Histórias Fase 2** | (US-05/06 Fase 1; ops infra em P5) |

---

## P4 — Worker / Sistema — *reuso + delta S3*

| Campo | Descrição |
|---|---|
| **Papel** | Celery em ECS Fargate |
| **Objetivo** | Consumir `ingerir_clientes` com `{lote_id, bucket, chave}`, ler S3, atualizar RDS |
| **Motivações** | Desacoplar API; processar na cloud sem volume compartilhado |
| **Dores** | Credenciais S3; objeto ausente; retries |
| **Comportamento** | Task role com least-privilege S3; status PENDENTE→PROCESSANDO→CONCLUIDO\|ERRO |
| **Histórias Fase 2** | US-AWS-03 |

---

## P5 — DevOps / Cloud — *nova*

| Campo | Descrição |
|---|---|
| **Papel** | Provisiona e opera o ambiente **dev** AWS |
| **Objetivo** | Terraform apply via GHA, smoke, dump/restore, trilha de mudança e rollback note |
| **Motivações** | Stack previsível, barata (single-AZ), segura o bastante para demo/dev |
| **Dores** | Apply quebrado; secrets vazados; sem procedimento de restore |
| **Comportamento** | Abre PR → GHA build/push/apply; valida smoke; documenta rollback |
| **Histórias Fase 2** | US-AWS-05, US-AWS-06, US-AWS-07, US-AWS-08 |

---

## Mapa Persona → Histórias Fase 2

| Persona | Must (Fase 2) |
|---|---|
| P1 Integrador | US-AWS-01, US-AWS-02, US-AWS-04 |
| P4 Worker | US-AWS-03 |
| P5 DevOps | US-AWS-05, US-AWS-06, US-AWS-07, US-AWS-08 |
| P2 / P3 | Sem histórias novas dedicadas; usam Gateway+Key (US-AWS-01) + US Fase 1 |
