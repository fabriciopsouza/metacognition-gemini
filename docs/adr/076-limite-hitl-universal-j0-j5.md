# ADR-076 — Limite Estrito de HITL (MAX_ROUNDS=3) em Junções J0-J5 (Suplanta ADR-011 parcial)

- Data: 2026-06-07
- Contexto: Metacognição (Cross-IA) / QA Bicelular
- Status: **Aceito** (ratificado via diretriz de dono de projeto)

## Contexto e Problema

O ADR-011 definiu a arquitetura bicelular de QA com as junções J0-J5 sendo *forward-only*, mas permitindo *"iterações ilimitadas DENTRO da junção até PASS binário"*. 
Isso cria um ponto cego perigoso: o agente (seja no papel de *developer* ou *qa-critic*) pode entrar em um "hallucination loop", onde tenta corrigir o mesmo erro repetidamente sem sucesso, queimando tokens e contexto indefinidamente por não possuir uma válvula de escape para intervenção humana (HITL) no processo de desenvolvimento local. O limite de turnos (`MAX_ROUNDS = 3`) existia no framework (ADR-069), mas estava restrito às trocas Cross-IA no Hub.

## Decisão

1. **Fim das Iterações Ilimitadas:** A cláusula "iterações ilimitadas DENTRO da junção" do ADR-011 está oficialmente **suplantada**.
2. **Limite Universal (N=3):** Qualquer junção de entrega (J0 a J5) ou avaliação de *Process-Critic* possui um limite estrito de `MAX_ROUNDS = 3` tentativas de correção para o mesmo bloco de código ou design.
3. **HITL Obrigatório:** Ao falhar pela 3ª vez em transpor o gate binário ou resolver o apontamento do QA, o sistema entra em estado de bloqueio (`escalation=pending`). O fluxo é interrompido e exige o Override Humano explícito para indicar a direção correta ou assumir o risco (PASS forçado).
4. **Aplicação Determinística:** Os scripts de *hooks* do framework (`cross_ai_gate.py`, `consistency-gate`, etc.) e a diretriz fundamental (`GEMINI_Metcognition.txt`) passam a operar sob esse teto universal.

## Consequências

- **Positivas:** Interrupção precoce de loops delirantes; redução dramática de custo por queima de contexto; garantia de que o humano no loop seja consultado em problemas realmente difíceis em vez da máquina fingir progresso.
- **Negativas:** Exigirá mais interrupções para o desenvolvedor principal em tarefas nas quais o agente antes tentaria resolver sozinho ao longo de dezenas de iterações. O ganho em previsibilidade compensa este custo.

**Emenda ao ADR-011:** A seção de dinâmica interna ("DENTRO da junção") do ADR-011 deve ser lida a partir de agora com o teto de 3 iterações imposto por este documento.
