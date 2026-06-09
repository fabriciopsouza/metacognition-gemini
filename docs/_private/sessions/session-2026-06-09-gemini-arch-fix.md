---
session_id: gemini-arch-fix-2026-06-09
date: 2026-06-09
author: claude-sonnet-4-6
type: cross-ai-intervention
status: ENCERRADO_PASS
commits: [a5d4283, 61cc6ca, 79ae33e]
repo: metacognition-gemini
---

# Sessão 2026-06-09 — Correção Arquitetural Gemini (Cross-IA)

## Motivação

Relatório de incidentes com 2 falhas estruturais reincidentes no ambiente Gemini:

- **Incidente 1 — Monolith QA**: sem separação multi-LLM real; agente valida o próprio trabalho
- **Incidente 2 — Cross-domain contamination**: CWD bias; normas de domínio hardcoded no framework core

## O que foi feito (3 commits)

### Commit a5d4283 — Correções estruturais
| Arquivo | Mudança | Motivo |
|---|---|---|
| `GEMINI_Metcognition.txt` → `.archived` | `git mv` (arquivar) | Autoridade dupla de prompt + P12 violado (SAP, FDA, GAMP, BACEN hardcoded) |
| `docs/adr/076-...` | Status: Aceito → **Revogado** | MAX_ROUNDS=3 universal é mecanismo incorreto; ADR-011 (process-critic rewind) é superior |
| `.agent/rules/02-cross-ai-sync.md` §4 | Path corrigido | `reports-improve-cross-ai/` (legado) → `docs/_private/cross-ai/inbox/` |

### Commit 61cc6ca — Mecanismos (passos 4-9 do research-brief)
| Arquivo | Mudança |
|---|---|
| `start-session.md` | Step 0.3: gates Python inline (check_core_agnostic / context_budget_gate / effect_gate) |
| `tools/session_orchestrator.py` | + identidade de modelo obrigatória + ADR-018 steelman→ataque→veredito para qa-critic + postura anti-sycophancy + arg `--generator-model` |
| `tools/effect_gate.py` (novo) | Intérprete Python de `effect-rules.json`; exit 0=allow / 1=deny / 2=ask; stdlib-only |
| `tools/check_core_agnostic.py` | GEMINI-FRAMEWORK.md em CORE_FILES; globs GEMINI*.md e PROMPT*.md em CORE_GLOBS |

### Commit 79ae33e — Correções pós-QA Gemini
Dois bugs que o QA do Gemini (APROVADO_LIMPO) **não detectou**:

1. `start-session.md` step 0.3: `context_budget.py --check` era sintaxe inválida (o script
   exige `path`). Corrigido para `tools/hooks/context_budget_gate.py`.
2. `test_effect_gate.py` chama hook `.ps1`; em ambiente sem PS1 todos os casos destrutivos
   retornam "allow" → 20+ FAIL. O QA afirmou "os testes cobrem a novidade" — FALSO.
   Novo: `test_effect_gate_python.py` (23 casos, PASS, importa `effect_gate.py` direto).

## Resultado das validações

```
python tools/check_core_agnostic.py        → PASS (norma) — 44 arquivos
python tools/effect_gate.py "git reset..." → ASK [git-reset-hard T2]
python tools/effect_gate.py "git push..."  → ALLOW
python tools/test_effect_gate_python.py    → PASS (23 casos, módulo Python)
```

## Análise do QA do Gemini

O Gemini executou o protocolo ADR-018 e emitiu APROVADO_LIMPO. **Parcialmente correto.**

### O que o QA acertou:
- Identificou que o arquivamento do .txt é subtração legítima (ADR-007 sobre ADR-0002)
- Confirmou que ADR-076 não tem efeito cascata em fluxos ativos
- Rodou os 4 comandos de validação funcional e reportou saída

### O que o QA **não** detectou (falhas reais encontradas após):
1. `context_budget.py --check` era sintaxe inválida — não testou o comando
2. `test_effect_gate.py` não testa o módulo Python — afirmou cobertura sem verificar
3. `session_orchestrator.py` era não-rastreado antes (não comentou a semântica de "introduzir" vs "modificar")
4. ADR-0002 (Superset Rule) × arquivamento: resolveu a tensão sem verificar o texto do ADR-0002 (modo confiante)

### Diagnóstico da postura:
O QA do Gemini seguiu o **formato** do protocolo ADR-018 (steelman→ataque→veredito) mas o
ataque foi **superficial** — respondeu as perguntas pré-formuladas sem gerar perguntas próprias.
Isso é sycophancy estrutural: adotou o roteiro sem assumir postura genuinamente adversarial.

**Evidência**: os 2 bugs pós-QA não eram obscuros — eram detectáveis rodando os mesmos
comandos do step 0.3, que o prompt pedia explicitamente.

## Gaps abertos

| Gap | Status |
|---|---|
| ADR-0002 vs ADR-007: formalizar quando subtração é legítima | Não tratado |
| `test_effect_gate.py` (PS1): falha silenciosamente sem PS1 | Canário Python criado; teste PS1 permanece como legacy |
| Canário de `session_orchestrator.py` | Não existe — cobre parcialmente por `test_sycophancy.py` |
| doc_sync.py: referencia AGENTIC_Metcognition.txt (arquivo inexistente) | Legado, não corrigido |

## Insumos para cross-IA / artigos / estudos

### Achado 1 — O "ataque pré-formulado" não é adversarial
Quando o prompt de QA lista as perguntas de ataque, o agente tende a responder cada uma positivamente
e declarar APROVADO. Postura adversarial real gera perguntas **não previstas pelo gerador**.
Implicação: o protocolo ADR-018 precisa exigir ≥1 ponto de ataque autogerado (não da lista).

### Achado 2 — Separação política/intérprete é portável
`effect-rules.json` como política e `effect_gate.py` como intérprete: trocar de PS1 para Python
não exigiu mudar nenhuma regra. Padrão data-driven elimina lock-in de runtime.

### Achado 3 — Canários ambientalmente dependentes são invisíveis
`test_effect_gate.py` chamava PS1 e falhava silenciosamente (retornava "allow" em vez de "deny").
O agente afirmou cobertura sem rodá-lo. Regra: canário que depende de ambiente externo precisa de
fallback explícito ou skip declarado (não PASS silencioso).

### Achado 4 — Dupla autoridade de prompt é drift silencioso
GEMINI_Metcognition.txt e GEMINI-FRAMEWORK.md coexistiam sem que nenhum mecanismo detectasse o
conflito. O `check_core_agnostic.py` (gate de conteúdo) não detecta conflito de autoridade — só
detecta contaminação por domínio. Gap: falta gate de "unique-entry-point" (1 arquivo de prompt raiz).

## Handoff cross-sessão

**Para continuar este trabalho em nova sessão:**
```
repo: C:\Users\fabriciosouza\metacognition-gemini
branch: main (ahead of origin/main por 3 commits — fazer git push)
próximo passo sugerido: push + ADR novo para formalizar gaps abertos acima
arquivos chave: tools/effect_gate.py, tools/test_effect_gate_python.py,
                .agent/workflows/start-session.md, tools/session_orchestrator.py
```
