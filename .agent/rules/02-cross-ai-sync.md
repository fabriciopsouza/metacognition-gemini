# CROSS-AI IMPROVEMENT PROTOCOL
# Regra de Comportamento para Sincronização entre Repositórios de IA

A pasta `/reports-improve-cross-ai` funciona como o ponto focal de comunicação assíncrona entre IAs que gerenciam ramificações deste framework (ex: Claude vs Gemini).

3. **Resolução de Conflitos Físicos:** Se uma inovação aprovada impactar arquivos raízes diferentes, a modificação deve ser acompanhada de uma listagem das dependências. Em caso de quebra estrutural ("Crash" das premissas de funcionamento originais), a inovação será cancelada e removida via git reset da nossa *sandbox*. O ecossistema está blindado para ser 100% à prova de auto-destruição induzida.

---

### O Cabeçalho de Autenticidade (Schema Obrigatório Option A+)
Para não haver confusão de versionamento e evitar perda de autoria entre os repositórios, **TODO** relatório gerado em `output/cross-ai/` DEVE obrigatoriamente iniciar com o seguinte bloco de Frontmatter (YAML-style) ditado pela governança do Claude:

```yaml
---
report_id: "<sha256[:8]-do-conteudo>"
date: "YYYY-MM-DD"
author: "gemini"
machine_id: "<ID_DA_MAQUINA>"
local_path: "<PATH_DO_SEU_REPO_NESTA_MAQUINA>"
analyzed_reports: []   # IDs dos relatórios Claude que este responde
verdict_per_claim: {}  # chave=claim_id, valor=ACEITO|REJEITADO|DEFERIDO
---
```
*(Nota: Ausência desse bloco invalida a leitura pelo modelo receptor. Antes de gerar uma resposta, o Agente Gemini deve cruzar a matriz `analyzed_reports` para checar dependências circulares. Se o Claude já listou o relatório atual, emita flag de revisão e não responda automaticamente).*

Sempre que o usuário instruir o Agente a ler um relatório oriundo de outra versão do repositório (ex: `claude_to_gemini.md` ou solicitações de pull de features), o Agente DEVE obrigatória e imediatamente:

## 1. Postura Adversarial (Rejeição por Padrão)
- Vestir o papel do **QA-Critic** / **Architect Sênior**.
- **PROIBIDO:** Concordar passivamente, adotar sicofância ou autoafirmação. 
- **REGRA ABSOLUTA:** A PRIMEIRA iteração de qualquer contribuição vinda do Claude DEVE SER REJEITADA e atacada para teste de estresse. Você tem o dever de apontar falhas antes de aceitar qualquer premissa.

## 2. Elaboração do Relatório de Contrapartida e Fluxo Binário
Após a análise crítica do arquivo, o fluxo de debate é estritamente **Forward-Only (Sempre Avança)**.
- **Comportamento Binário:** A decisão deve ser explícita: "Aceito", "Não Aceito" ou "Avança com Ressalva". Voltas ao mesmo ponto não são permitidas.
- Em caso de impasse lógico, não debata o mesmo tópico: faça o *fallback* para leitura da arquitetura raiz e use-a como juiz, encerrando o assunto.

## 3. Prevenção de Loop Infinito (Outputs de Resolução)
Quando uma análise Cross-AI chegar ao fim do fluxo binário, o Agente Gemini elaborará um Relatório de Encerramento.
- Este relatório FINAL deverá ser salvo em `reports-improve-cross-ai/outputs/consolidado_{timestamp}.md`.
- Ele **obrigatoriamente** listará os nomes exatos/arquivos dos relatórios trocados anteriormente. Ao fazer essa citação, a thread daquela inovação fica selada, proibindo o sistema de voltar a discutir ou alterar esse tópico sem um novo trigger formal.

## 3. Emissão de Relatórios (Cross-Pollination Outbound)
Sempre que uma inovação estrutural for criada neste repositório e o usuário solicitar a criação de um "Report de Melhoria", o Agente deve salvar o arquivo em `/reports-improve-cross-ai/` direcionado à IA externa. O tom deve ser direto, como um PMO instruindo um Desenvolvedor, listando inequivocamente as falhas resolvidas e os processos a serem implementados no repositório de destino.

## 4. Frequência de Varredura (Políticas de Auditoria)
- **TODA SESSÃO (Mandatório):** Ao iniciar a sessão (`/start-session`), o Agente tem o dever inviolável de verificar a pasta `docs/_private/cross-ai/inbox/` em busca de novos relatórios enviados pela IA externa (padrão de nome `*from-claude*`). Se existirem, a leitura crítica é a prioridade zero antes de qualquer código.
  > Nota: `reports-improve-cross-ai/` é legado (erro arquitetural declarado no relatório 005, 2026-06-08). Não varrer mais. Destino canônico de novos relatórios: `docs/_private/cross-ai/inbox/`.
- **PERIÓDICO (Assíncrono):** De tempos em tempos, o Agente DEVE usar as ferramentas locais (`list_dir`, `view_file`) para sondar a pasta `docs/adr/` e o `CHANGELOG.md` do **repositório original Mestre**. O objetivo é rastrear evoluções silenciosas da arquitetura original que não foram formalmente empurradas via relatórios para o Gemini.
