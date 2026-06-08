# Relatório Cross-IA 005 — Falhas e Propostas Arquiteturais: Projeto ATD-36246 FEFO/FIFO

**Origem:** Claude (Antigravity IDE) — Sessões 1 e 2
**Destino:** Framework Metacognição (metacognition-framework / metacognition-gemini)
**Data:** 2026-06-08
**Projeto de origem:** Correção FEFO/FIFO SAP EWM — PPM 6376237 / ATD-36246
**Programa ABAP:** `ZRWM0028_MOVIMENTACAO_DEPOSITO`

---

## Contexto

Durante duas sessões de trabalho no projeto ATD-36246 (correção de algoritmo FEFO/FIFO em ABAP SAP EWM), foram identificadas 7 falhas sistêmicas de agente — catalogadas como FA-01 a FA-07 — e 5 propostas de evolução arquitetural para o framework. Este relatório consolida os insights para ingestão pelo framework mãe e pelo Cross-IA Hub (Gemini/Claude).

---

## Taxonomia de Falhas de Agente (FA-01 a FA-07)

| Código | Nome | Descrição | Sessão |
|---|---|---|---|
| FA-01 | Falso-PASS | Aprovar entregável sem validação cruzada contra spec completa | 1 |
| FA-02 | Viés de Oráculo | Tratar consultoria/terceiro como fonte absoluta sem verificação | 1 |
| FA-03 | Miopia de Escopo | Analisar trecho sem verificar estado global do programa | 1 |
| FA-04 | Elicitação Prematura | Perguntar ao humano o que o código responderia se lido | 2 |
| FA-05 | Parada Inter-Papel | Aguardar instrução humana em transição automática Developer→QA | 2 |
| FA-06 | Ausência de Resiliência | Não salvar estado, sem timer, sessão vulnerável a queda/freeze | 2 |
| FA-07 | Troca de Modelo Não-Automatizada | Developer e QA no mesmo modelo/sessão sem mecanismo de separação | 2 |

**Uso recomendado**: O `qa-critic` deve checar ao final de cada bloco se algum FA-xx ocorreu e reportá-lo explicitamente no output. A taxonomia deve ser adicionada ao checklist padrão do `qa-critic/SKILL.md`.

---

## Proposta E1 — Hook: Auto-transição Developer → QA-Critic

**Problema (FA-05)**: O agente para entre papéis e aguarda instrução humana.

**Proposta**: Adicionar ao `developer/SKILL.md`:

```markdown
## Pós-entrega obrigatório (Developer)
1. Anunciar: "Código entregue. Iniciando QA-Critic."
2. Gerar Prompt Package (ver E5).
3. Ativar qa-critic sem aguardar instrução.
4. Só parar se qa-critic retornar PASS (aprovado) ou REWIND (confirmado pelo usuário).
```

**Impacto**: Elimina FA-05. A janela de escape de bugs entre Developer→QA fecha sem depender de atenção humana.

---

## Proposta E2 — Regra §D-01: Ler Antes de Elicitar

**Problema (FA-04)**: O agente pergunta ao humano sobre comportamento observável no código sem ter lido o trecho.

**Proposta**: Formalizar no `developer/SKILL.md` e `qa-critic/SKILL.md`:

> **§D-01 — Ler Antes de Elicitar**: Antes de qualquer pergunta ao humano sobre comportamento de variáveis, estado de estruturas ou fluxo de execução, o Developer DEVE executar `view_file` (startLine/endLine precisos) no trecho relevante. Perguntas sobre comportamento observável no código são vetadas sem essa leitura comprovada. Perguntas ao humano são permitidas apenas para: (a) regras de negócio não-inferíveis do código, (b) intenção do usuário sobre comportamento desejado, (c) contexto de ambiente/sistema ausente dos artefatos.

**Motivação**: Perguntar ao humano o que o código diz é um Falso-`[DESCONHECIDO]` — o agente não leu, mas poderia ter lido.

---

## Proposta E3 — Protocolo Anti-Congelamento Determinístico

**Problema (FA-06)**: Ausência de mecanismo de resiliência. Em caso de queda de conexão, travamento do IDE ou timeout, todo o contexto em progresso é perdido.

**Proposta**: Tornar obrigatório no workflow squad:

| Gatilho | Ação automática | Ferramenta |
|---|---|---|
| Início do bloco Developer | Registrar estado inicial | Append em `history.md` |
| Entrega do patch | Checkpoint: artefatos + decisões | Append em `history.md` |
| Transição de papel | Handoff compacto inline | Seção no relatório |
| Sessão > 2 turnos sem artefato entregue | Timer de heartbeat | `/schedule` |
| Início de retomada | Leitura de `history.md` | `view_file` — passo 1 obrigatório |

**Adicionalmente**: Artefatos gerados durante uma sessão devem ser copiados para o workspace (controle de versão) antes de encerrar. Artefatos em `Downloads/` ou fora do repo são invisíveis ao próximo `/start-session`.

---

## Proposta E4 — Troca de Modelo Entre Papéis (FA-07)

**Problema**: Developer e QA-Critic rodam no mesmo modelo e sessão. O framework prevê "modelo diferente quando possível" (AGENTS.md §QA bicelular), mas não havia mecanismo para garantir.

**Análise técnica** `[CONFIRMADO]`:
- Não é possível criar nova sessão programaticamente de dentro da sessão ativa no Antigravity IDE.
- O perfil GitHub `fabriciopsouza` é acessível, mas o repo `metacognition-framework` está privado/inexistente — impossibilitando carga remota do framework.

**Camadas de solução**:

| Camada | Abordagem | Status |
|---|---|---|
| 1 — Hoje | Prompt Package gerado pelo Developer; usuário cola em nova sessão/modelo | Implementável imediatamente |
| 2 — Script | `qa_orchestrator.py` chama API (Anthropic/Google) com modelo diferente | Backlog — ~30 min, requer chave API |
| 3 — IDE API | Script cria sessão via endpoint local do IDE | `[DESCONHECIDO]` — API não documentada |

**Recomendação**: Implementar Camada 1 como padrão obrigatório (via E5). Camada 2 como próxima feature do framework.

---

## Proposta E5 — Prompt Package Obrigatório (Handoff Developer → QA)

**Problema**: O handoff entre Developer e QA dependia de provocação humana (FA-05 + FA-07).

**Proposta**: Todo output do Developer deve incluir obrigatoriamente um "Prompt Package" no formato:

```
=== PROMPT PACKAGE — QA-Critic ===
Papel: qa-critic (adversarial)
Contexto: [resumo do que foi feito]
Mudanças: [lista de mudanças com linha]
Checklist: [C1..Cn com cenários de edge case]
FA-CHECK: [FA-01 a FA-07 ocorreram?]
Critério de PASS: [definição binária]
Critério de REWIND: [definição binária]
===
```

**Este pacote serve para**:
1. QA-Critic na mesma sessão (quando não há outro modelo disponível)
2. Nova sessão com modelo diferente (Camada 1 da E4)
3. Registro permanente de decisões no `history.md`

---

## Proposta E6 — Artefatos em Workspace (Não em Downloads)

**Problema (FA-06 derivado)**: O `relatorio_execucao.md` foi criado em `Downloads/`, fora do workspace git. Invisível ao próximo `/start-session`.

**Regra proposta para o framework**:

> Todo artefato gerado durante uma sessão squad DEVE ser criado dentro do workspace git (`c:\Users\fabriciosouza\metacognition-gemini\` ou equivalente). Artefatos fora do workspace são tratados como temporários e não fazem parte do histórico do projeto. O Developer deve criar/mover artefatos para o workspace antes de encerrar o bloco.

**Estrutura sugerida**:
```
metacognition-gemini/
  reports-improve-cross-ai/   ← relatórios cross-IA numerados (00x-...)
  case-study/                 ← estudos de caso completos por projeto
  docs/adr/                   ← decisões arquiteturais
  history.md                  ← log contínuo de sessões
```

---

## Proposta E7 — Resolução do GitHub 404 (framework inacessível remotamente)

**Problema**: A carga remota do AGENT-FRAMEWORK.md falha com 404.

**Diagnóstico** `[CONFIRMADO]`:
- URL tentada: `https://raw.githubusercontent.com/fabriciopsouza/metacognition-framework/main/AGENT-FRAMEWORK.md`
- Perfil `fabriciopsouza` existe e tem 32 repos públicos
- O repo `metacognition-framework` **não aparece na listagem pública** → provavelmente **privado**
- Fallback OneDrive local funciona: `C:\Users\fabriciosouza\OneDrive - Natulab Laboratorio S.A\Documents\Meus Repositórios\metacognition-framework\AGENT-FRAMEWORK.md`

**Ações recomendadas (para o dono do projeto)**:
1. Verificar visibilidade do repo `metacognition-framework` no GitHub → tornar público **ou**
2. Adicionar o Antigravity IDE como colaborador com acesso de leitura **ou**
3. Publicar o `AGENT-FRAMEWORK.md` em um Gist público para carga sem autenticação

**Fallback canônico até resolução**:
```
Primário:   OneDrive local (C:\Users\fabriciosouza\OneDrive - Natulab Laboratorio S.A\...)
Secundário: raw.githubusercontent.com (quando repo for público)
Terciário:  modo degradado — anti-alucinação + CONFIRMADO/INFERIDO/DESCONHECIDO
```

**Esta proposta deve ser escalada para o dono do projeto como débito técnico de infraestrutura.**

---

## Registro de Provocações do Usuário (HITL que gerou este relatório)

As seguintes intervenções humanas foram necessárias e NÃO deveriam ter sido:

| Turno | Provocação | FA gerado |
|---|---|---|
| "cadê então? está parando e ficando parado" | Agente parou após Developer sem ir para QA | FA-05 |
| "isso deve ser feito antes de perguntar ao humano" | Agente perguntou sobre variáveis sem ler código | FA-04 |
| "ferramentas para impedir congelamentos deveria ser determinístico" | Sem checkpoint nem heartbeat | FA-06 |
| "ao mudar de papel, deveria ser alterado o modelo" | Sem mecanismo de troca de modelo | FA-07 |
| "onde fica o relatório? fica acessível?" | Relatório criado em Downloads, fora do workspace | FA-06 derivado |
| "não deveria ser determinístico?" | Cópia para workspace não foi automática | FA-05 + FA-06 |

**Conclusão**: Todas as 6 intervenções eram evitáveis com implementação das propostas E1–E7.
