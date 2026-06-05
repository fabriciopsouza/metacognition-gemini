# PROTOCOLO DE INTEGRAÇÃO (CROSS-AGENT SYNC)

Este repositório (`metacognition-gemini`) atua como um *Downstream Público*. Ele herda sua lógica de arquitetura do repositório original Master (exclusivo para o LLM Claude, que detém o cofre e dados sensíveis).

Sempre que o usuário fornecer a este Agente Gemini um documento ou mensagem encabeçada por `# SYNC REPORT: CLAUDE TO GEMINI`, o Agente DEVE entrar imediatamente em **Modo de Integração Adversarial**.

## Regras de Recebimento do Sync Report

1. **Postura Adversarial:** O Gemini **NÃO DEVE** acatar as atualizações do Claude cegamente. O Claude não compreende completamente as ferramentas nativas do ecossistema Gemini (como Artifacts e Antigravity Ide Workspace). O Gemini deve analisar a essência da atualização e traduzi-la para a sua própria governança (`GEMINI-FRAMEWORK.md`).
2. **Respeito à Premissa:** Os *insights*, metodologias, processos e experiências (o "Porquê") enviados pelo Claude são sagrados. A adaptação Gemini pode mudar o *Como*, mas nunca descartar o problema lógico apontado pelo original.
3. **Validação de Sicofância:** O Gemini deve se perguntar: *"A atualização proposta pelo Claude tenta facilitar demais o processo? Se sim, como eu blindo isso no Gemini para que o modelo não crie mocks ou pule validações?"*
4. **Relatório de Merge:** Após atualizar o repositório Gemini Edition com as novidades do Claude, o Agente Gemini deve devolver um sumário estruturado chamado `[MERGE EXECUTADO]`, listando quais arquivos foram alterados e como a funcionalidade do Claude foi engessada nas amarras do Gemini.
