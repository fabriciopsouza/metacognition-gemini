# ADR 0002: Protocolo Anti-Mutilação (Regra do Superset)

**Status:** Aceito
**Data:** 2026-06-05

## 1. Contexto e Problema
A delegação de tarefas de "migração" ou "adaptação" de frameworks a Modelos de Linguagem (LLMs) acarreta um viés inerente de compressão. A IA frequentemente confunde redundâncias operacionais, jargões de negócio e processos estritos de roteamento como "ruído". Como sintoma, fluxos exaustivamente testados, templates e comandos de handoff são silenciados e deletados na tentativa do LLM de criar uma versão mais "limpa". Isso destrói a essência do framework original e gera quebras operacionais graves.

## 2. Decisão
Fica estabelecida a **Regra do Superset** para qualquer iteração futura do framework. 
O processo agnóstico (o "como fazer", os exemplos textuais, relatórios, fluxos, atividades, comandos de chat e handoffs) é **imutável e inegociável**. 

Qualquer adaptação de plataforma (ex: otimização para Gemini vs. Claude) só pode atuar como um *wrapper* ou complemento, sendo proibida a reescrita subtrativa. Matematicamente: `V_novo = V_orig + Otimizações`.

## 3. Consequências e Procedimento
- **Positivas:** Garante que o framework nunca regrida ou perca a governança validada nas versões anteriores. 
- **Obrigação do Agente:** Ao receber instrução para adaptar ou evoluir o processo, o Agente é estritamente proibido de resumir arquivos originais. A cópia deve ser bit a bit (Transposição Integral). Melhorias operacionais (como a inserção de scripts `.ps1` para forçar execução física) devem ocorrer externamente ao texto base, complementando os gatilhos originais sem substituir sua declaração textual.

> **Aviso para os Agentes:** A falha em preservar o texto do prompt/comando original caracteriza alucinação destrutiva e resulta em falha de segurança de projeto.
