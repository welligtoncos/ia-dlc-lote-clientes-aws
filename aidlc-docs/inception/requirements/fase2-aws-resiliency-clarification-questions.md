# Esclarecimentos Resiliency — Fase 2 AWS

A extensão **Resiliency Baseline** foi ativada (Q12=A).  
Antes de **aprovar** o documento de requisitos, responda:

---

## Question CQ1 — RTO/RPO e estratégia de DR (RESILIENCY-02)

Quais são os alvos de RTO/RPO e a estratégia de Disaster Recovery para o ambiente **dev** deste ciclo?

A) Dev sem DR formal: RTO/RPO **best-effort**; estratégia **Backup & Restore** manual (snapshot RDS + versionamento S3); aceitável perder dados recentes em falha total da conta/região

B) RTO ≤ 8h, RPO ≤ 24h; Backup & Restore automatizado (snapshots RDS diários + retenção S3)

C) RTO ≤ 1h, RPO ≤ 15min; Pilot Light / Warm Standby (mais custo — pode conflitar com Q4=dev single-AZ barato)

D) Outro (descreva RTO, RPO e estratégia após [Answer]:)

[Answer]: A

---

## Question CQ2 — Criticidade do workload (RESILIENCY-01)

Classificação de criticidade do serviço de ingestão neste ciclo **dev**:

A) **Low** — ambiente de desenvolvimento/demo; indisponibilidade sem impacto de receita

B) **Medium** — usado por stakeholders internos com alguma expectativa de uptime

C) **High / Critical** — já tratado como produção

D) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question CQ3 — Topologia regional (RESILIENCY-08)

A) **Single-region** `us-east-1`, single-AZ (alinhado a Q4=A custo baixo)

B) Single-region multi-AZ (sobe custo; RDS Multi-AZ)

C) Outro (descreva após [Answer]:)

[Answer]: A

---

## Question CQ4 — Gerenciamento de mudanças (RESILIENCY-03)

Como governar mudanças neste workload (ambiente **dev**)?

A) Usar processo formal existente da organização (nomear ferramenta após [Answer]: — ex.: ServiceNow, Jira Change)

B) Sem processo formal — AI-DLC propõe leve: registro de mudança no PR/GHA + nota de rollback no README/runbook

C) Isento de change management formal neste ciclo (dev/Low; GHA apply automático é o mecanismo) — documentar isenção

D) Outro (descreva após [Answer]:)

[Answer]: B
