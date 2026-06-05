# SQUAD MASTER HOOK
# Este arquivo é o gatilho principal para o Modo Squad (Camada 2).

A presença deste arquivo na raiz do repositório ativa obrigatoriamente a leitura de:
1. `.agent/skills/pmo/SKILL.md` (Ponto de entrada).
2. `docs/briefing.md` (Contexto do projeto).
3. `docs/adr/` (Restrições de arquitetura).

## Comandos Ativos de Roteamento (Prompt Hooks):
Ao receber qualquer um destes comandos no chat, o Agente DEVE assumir o papel correspondente:
- `/start-session` -> Ativa PMO.
- `/feature-plan` -> Ativa Architect.
- `/implement` -> Ativa Developer.
- `/sap-change` -> Ativa SAP Specialist.
- `/bi-deliverable` -> Ativa BI Analyst.
- `/handoff` -> Gera Checkpoint Markdown.

> **[GARANTIA GEMINI]**: A regra do framework mestre determina a prioridade de ferramentas ("Tool-First"). Logo, o recebimento destes comandos em texto obriga o Agente a acionar o script `.ps1` complementar em `.agent/tools/` para validar a execução. O modelo de QA é estritamente separado.
