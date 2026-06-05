# SQUAD GEMINI: Roteamento de Projetos e Validação Adversarial
*Documentação de Operação Multi-agente v1.0.0-gemini (Herdada e escalada da Camada 2 do Metacognition Original v2.2.0)*

Este documento estabelece as regras para o **Modo Squad Nativo** no ecossistema Gemini. Enquanto no framework original os papéis de *Squad* eram virtuais, nesta edição eles se tornam restrições sistêmicas para contornar a sicofância e a prosa nativa.

## 1. O Problema da Prosa e a Solução Nativa

Para evitar que o Gemini ative o "viés de agradar" comum em chats, o Modo Squad abandona a dependência de "pedidos descritivos" e foca em **Gatilhos Estruturados**:

- Todo pedido usa ferramentas (`view_file`, `list_dir`) ao invés de suposições.
- A comunicação entre usuário e agente se dá pela edição de artefatos de plano e tarefas.

## 2. Separação Estrita de Papéis (A Inovação do QA Adversarial)

No repositório original (v2.2.0), o *QA-Critic* era um chapéu cognitivo do LLM. Aqui, exigimos a divisão obrigatória e física entre Criação e Validação.

### Papel 1: O Agente Desenvolvedor (Criador)
- **Regra Base:** O mesmo modelo do framework original (*File-First*, *Anti-Rename*). Aplica a Camada 1 (`GEMINI-FRAMEWORK.md`) estritamente.

### Papel 2: O Agente QA Critic (Adversarial)
- **Função Obrigatória:** O QA **DEVE** rodar em um modelo de IA separado do Desenvolvedor.
- **Implementação:** Se o Dev rodou em `Gemini Advanced`, o QA deve rodar em `Gemini Flash`.
- **Comportamento:** O QA não pode escrever código de features; ele só rejeita ou aprova diffs puramente com base em matemática e *edge cases*.

## 3. Workflow de Execução Direta

Conforme o original de Claude v2.2.0, o fluxo de projeto em múltiplas etapas segue o ciclo de:
1. Plano via artefato aprovado.
2. Implementação com *Ownership* (parada de bloqueio se houver erro).
3. QA Adversarial de modelo distinto valida o artefato de *Walkthrough* gerado pelo Dev.
