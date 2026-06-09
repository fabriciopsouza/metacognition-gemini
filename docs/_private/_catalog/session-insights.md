## Insights do Corpus de Aprendizado

> ADR-068 · Catálogo agnóstico de processo · Rebuild: `python tools/knowledge_catalog.py --build`

### [86147e87] 2026-05-27 · 2026-05-27-plano-otimizacao-framework.md
> Rota: `squad` · Skills: dev, discovery, architect, qa-critic, docops, ux, research, spec, evals

**Gaps declarados:**
- *Aprendizado/memória de fracassos (ex-G9):* reusar /checkpoint + history.md + ADR.
- *Nada parado/pausado/planejado esquecido (ex-G11):* reusar start-session + history.md.

### [5c5384b4] 2026-06-06 · execution-report-2026-06-06-cross-ai.md
> Rota: `desconhecido` · Skills: dev, qa-critic, research

**Lições por skill:**
- **dev:** marker no repo é **forjável por cópia** → identidade tem de ser ancestralidade git (autoridade),
- **qa-critic:** rodar SEMPRE após escrever, em modelo isolado; pega bug em código que o autor já normalizou.
- **anti-loop / sistemas distribuídos:** terminação de crítica mútua exige **quiescência/ponto-fixo**
- **arquitetura de spread:** fonte única (master) → sombras (export); sombras **só devolvem aprendizado**;
- **honestidade:** `deep-research` voltou vazio → **não fabricar fonte**; mecanizar de 1º princípios e declarar.

**Gaps declarados:**
- repo-identity-gate é ADVISORY, não enforcement: hooks são vetados pelo Kaspersky nesta máquina →
- Hub privado cross-IA não provisionado (falta URL/repo do hub e do Gemini-mãe).

### [bde29fa0] 2026-06-03 · execution-report.md
> Rota: `squad` · Skills: dev, discovery, architect, qa-critic, docops, ux, research, spec

**Melhorias:**
- Honestidade da vitrine deixou de ser prosa → mecanizada (gates h/i de drift; detector hedge-aware).
- Resiliência a EDR em camadas (Python+fallback, nudge, pré-push) — uma config cobre admin-Kaspersky/admin-sem-Python/cross-platfor…
- Auditor de liveness universal (manifesto) → falha de hook nunca silenciosa.

**Boas práticas:**
- file-first salvou 2×: descobriu que a vitrine não flui pelo web_export (corrigiu o escopo do F2) e que a feature de report já exi…
- Testar contra arquivos reais (não teoria) revelou falsos-positivos do léxico (garante-gh, jamais-inventar-diretiva, não-inventada…
- Provar que o gate MORDE (teste negativo), não só que passa.

**Lições por skill:**
- **dev:** gate determinístico (regex/arquivo) > LLM-no-CI quando o critério é objetivo; fail-closed > fail-open em gate de confiança; carim…
- **discovery:** sempre checar se a feature **já existe** antes de construir (régua §0 economizou ~70% do ADR-062); inventário por risco (explorer…
- **architect:** EMENDA de ADR existente > ADR novo quando o gene já está lá; aplicar ADRs anteriores compõe ganho não-imediato (021/030/044 reusa…
- **qa-critic:** hipótese-default-bug pega drift que o autor normaliza; provar vazamento/bite, não só ausência; revisão estática quando não dá pra…
- **research/spec:** decisão regulada (LGPD/acesso) é gate humano **mesmo sob autonomia** (high-stakes × execução, ortogonais) — perguntar as 3 bifurc…

**Gaps declarados:**
- sync-global/framework-boot (boot machinery, este último GLOBAL fora do repo) podem ser vetados e não são auto-auditados → coberto…
- Anonimização por regex (learnings_public) não-exaustiva: token fora do map E da denylist passa (declarado em LIMITS).
