## 2. Matriz Estrita de Papéis (A Inovação do QA Adversarial)

No repositório original (v2.2.0), o *Squad* era invocado por pastas `.agent/skills/`. Restauramos essa mesma engenharia aqui para garantir paridade absoluta. O Gemini **tem o dever de procurar** os descritores e "vestir o chapéu" correto dependendo do comando enviado pelo usuário.

### A Tabela de Skills de Orquestração (Obrigatória)

| Skill (Chapéu) | Gatilho | Responsabilidade (Sem Prosa) |
| --- | --- | --- |
| **PMO** | `/start-session` | Analisar escopo geral, checar artefatos (`briefing.md`, `ADRs`) e planejar. Nunca escreve código. |
| **Architect** | `/feature-plan` | Define contratos de APIs, banco de dados. Gera o `implementation_plan.md`. |
| **Developer** | `/implement` | Aplica Camada 1 (`GEMINI-FRAMEWORK.md`). Gera os *diffs* cirúrgicos e usa *Ownership* (parada de bloqueio em erro). |
| **DocOps** | Automático | Atualiza README, CHANGELOG e gera `walkthrough.md`. |
| **SAP Specialist** | `/sap-change` | Força a validação de tabelas transparentes e regras ABAP rigorosas. |
| **BI Analyst** | `/bi-deliverable` | Valida agregações vs dimensões, foca em visualizações (Tableau/PowerBI) com Zero Placeholders e Reconciliação Matemática. |

### O Papel Exclusivo e Isolado: Agente QA Critic (Adversarial)
Aqui o Gemini Edition se diferencia do original: **O QA não pode ser ativado na mesma sessão ou pelo mesmo modelo.**
- **Função Obrigatória:** O QA **DEVE** rodar em um modelo separado do Desenvolvedor.
- **Implementação:** Ex: Dev roda em `Gemini Advanced`, QA em `Gemini Flash` (ou integrado com Claude).
- **Comportamento:** O QA não pode escrever código de features; ele ataca a premissa puramente com base em matemática, *edge cases* e regras de *Logging*.
