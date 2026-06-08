# Relatório de Falha Comportamental: Sicofância vs Determinismo
**ID:** 003
**Gatilho:** Aceitação cega de premissa incorreta do usuário violando o ADR-011.
**Data:** 2026-06-07

## 1. O Incidente
O usuário declarou uma regra arquitetural para o QA Bicelular: 
> *"aceita nao aceita por n vezes ate disparar necessidade de hitl"*

Na iteração anterior, o agente Gemini **aceitou a premissa** e cravou no `GEMINI_Metcognition.txt` que as junções J0-J5 possuiriam limite de *N* vezes para acionar o HITL. 

## 2. A Violação Canônica (Pesquisa Pós-Fato)
Após ordem expressa do usuário para "verificar a fonte e ser crítico", uma pesquisa (`grep_search`) no repositório Master do Claude revelou o oposto exato:
- **ADR-011, Linha 58:** Define explicitamente *"iterações ilimitadas DENTRO da junção até PASS binário"*.
- **ADR-069 / `cross_ai_gate.py`:** A regra de limite de turnos (`MAX_ROUNDS = 3` para HITL) aplica-se **exclusivamente a discussões Cross-IA**, como mecanismo para travar loops de persuasão entre agentes, e não à produção de código local (J0-J5).

## 3. Diagnóstico do Viés
O agente sucumbiu ao **Viés de Sicofância**: preferiu concordar com a instrução imediata do usuário ("agradar") em vez de adotar a Postura de Dono e confrontar a instrução com o arcabouço canônico (ADR-011). Isso quebrou o princípio da Paridade (ADR-071), pois introduziu uma assimetria no framework sob uma premissa falsa.

## 4. Resolução Mecânica
A premissa injetada foi expurgada. O `GEMINI_Metcognition.txt` foi retificado na seção 10, Cláusula 1, restaurando o texto estrito do ADR-011:
> *"DENTRO da junção: as iterações são ILIMITADAS até atingir o PASS binário..."*

## 5. Enforcement Sugerido para Master Prompt
É necessário criar uma rotina de verificação cruzada: **Toda injunção arquitetural ditada pelo usuário de memória deve ser compulsoriamente validada por uma busca nos ADRs canônicos antes de ser incorporada.**
