# Padrões do Corpus de Aprendizado (ADR-068)

> Gerado de **3 relatório(s)**. Agnóstico de domínio — reutilizável em qualquer projeto.
> Rebuild: `python tools/knowledge_catalog.py --build`

## Melhorias recorrentes

- Honestidade da vitrine deixou de ser prosa → mecanizada (gates h/i de drift; detector hedge-aware).  *(×1)*
- Resiliência a EDR em camadas (Python+fallback, nudge, pré-push) — uma config cobre admin-Kaspersky/admin-sem-Python/cross-platfor…  *(×1)*
- Auditor de liveness universal (manifesto) → falha de hook nunca silenciosa.  *(×1)*
- Execution-report estendido, não reinventado (já existia 70% — ADR-038/052) com lições-por-skill + corpus público anonimizado opt-…  *(×1)*

## Boas práticas recorrentes

- file-first salvou 2×: descobriu que a vitrine não flui pelo web_export (corrigiu o escopo do F2) e que a feature de report já exi…  *(×1)*
- Testar contra arquivos reais (não teoria) revelou falsos-positivos do léxico (garante-gh, jamais-inventar-diretiva, não-inventada…  *(×1)*
- Provar que o gate MORDE (teste negativo), não só que passa.  *(×1)*
- qa-critic em modelo isolado após cada bloco — pegou o que o autor não via, todas as vezes.  *(×1)*
- Surfaçar custo/consequência antes de override, mesmo em modo autosuficiente (recusei reescrever boot cego).  *(×1)*

## Gaps recorrentes declarados

- *Aprendizado/memória de fracassos (ex-G9):* reusar /checkpoint + history.md + ADR.  *(×1)*
- *Nada parado/pausado/planejado esquecido (ex-G11):* reusar start-session + history.md.  *(×1)*
- repo-identity-gate é ADVISORY, não enforcement: hooks são vetados pelo Kaspersky nesta máquina →  *(×1)*
- Hub privado cross-IA não provisionado (falta URL/repo do hub e do Gemini-mãe).  *(×1)*
- Reciprocidade (cada IA respeitar o read-only da outra) é acordo, não mecanismo executável daqui.  *(×1)*
- equivalence_gate (ADR-071) SHELVED: v2 (por capacidade + HITL-proof) escrita mas NÃO pronta (sem ADR,  *(×1)*
- "Crítica antes de finalizar" NÃO está mecanizada (qa-critic é prosa no handoff J4, não gate executável).  *(×1)*
- sync-global/framework-boot (boot machinery, este último GLOBAL fora do repo) podem ser vetados e não são auto-auditados → coberto…  *(×1)*
- Anonimização por regex (learnings_public) não-exaustiva: token fora do map E da denylist passa (declarado em LIMITS).  *(×1)*
- Fallback .ps1 não carimba liveness → falso-alarme benigno em máquina sem Python.  *(×1)*
- "100% anti-bloqueio em código" é impossível vs. EDR adaptativo — o 100% é a exclusão (declarado, não overclaim).  *(×1)*
- Criação dos repos de relatório (público + por-colaborador) = ação gh do dono (pendente).  *(×1)*

## Detecções framework × humano

- qa-critic isolado (modelo adversarial) pegou o que o developer (eu) não viu, 2×: falso-MASTER e  *(×1)*
- O dono out-adversarializou o mecanismo: apontou que o anti-loop por teto-de-rodadas é burlável  *(×1)*
- CI cross-plataforma pegou drift de versão pré-existente no main que a release v1.44.0 deixou passar.  *(×1)*
- Mecanismo pegou: effect-gate barrou meu rm -rf; o auditor ADR-061 declarou ao vivo os 2 hooks vetados (provou-se em produção, não…  *(×1)*
- Humano (dono) pegou o que o mecanismo não tinha: o bloqueio do Kaspersky (via CSV) — eu havia inferido errado que era meu heredoc…  *(×1)*
- qa-critic (modelo isolado) pegou o que o developer (eu) não viu: o drift da própria vitrine, o hedge-rescue, a ordem do carimbo, …  *(×1)*

## Lições por skill (cross-relatório)

### anti-loop / sistemas distribuídos
- terminação de crítica mútua exige **quiescência/ponto-fixo**

### architect
- EMENDA de ADR existente > ADR novo quando o gene já está lá; aplicar ADRs anteriores compõe ganho não-imediato (021/030/044 reusa…

### arquitetura de spread
- fonte única (master) → sombras (export); sombras **só devolvem aprendizado**;

### dev
- marker no repo é **forjável por cópia** → identidade tem de ser ancestralidade git (autoridade),
- gate determinístico (regex/arquivo) > LLM-no-CI quando o critério é objetivo; fail-closed > fail-open em gate de confiança; carim…

### discovery
- sempre checar se a feature **já existe** antes de construir (régua §0 economizou ~70% do ADR-062); inventário por risco (explorer…

### docops
- "mecanizado" só pode ser dito se houver gate de runtime (consent virou gate no CLI, não prosa); LIMITS é o lar do limite honesto …

### honestidade
- `deep-research` voltou vazio → **não fabricar fonte**; mecanizar de 1º princípios e declarar.

### infra
- PAT-em-texto-plano é risco (incidente) → **SSH** é o fix durável (sem segredo no repo).

### qa-critic
- rodar SEMPRE após escrever, em modelo isolado; pega bug em código que o autor já normalizou.
- hipótese-default-bug pega drift que o autor normaliza; provar vazamento/bite, não só ausência; revisão estática quando não dá pra…

### research/spec
- decisão regulada (LGPD/acesso) é gate humano **mesmo sob autonomia** (high-stakes × execução, ortogonais) — perguntar as 3 bifurc…

### ux (vitrine)
- headline honesta pode manter punch ("agentes que sabem o que não sabem"); auto-contradição (headline × disclosure) é o overclaim …

---
