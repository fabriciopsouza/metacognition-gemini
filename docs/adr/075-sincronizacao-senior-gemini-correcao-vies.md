# ADR-075: Sincronização Sênior do Framework Gemini e Correção de Viés (Fases 1 a 4)

## Status
Aceito

## Contexto
O framework Gemini foi inicializado com a infraestrutura basilar (`tools/` originais e uma premissa de metacognição). Contudo, auditorias revelaram que a inicialização original omitiu contratos críticos (como *QA Adversarial*, *Process Mapping*, *Context Engineering*), ignorou a importação do motor de *skills* (papéis especialistas e `_shared`) e não implementou gates de isolamento mecânico de forma rigorosa, produzindo uma instância com características de sicofância e viés de oráculo (afirmações não substanciadas, descarte silencioso de complexidade técnica).

## Decisão
Implementamos um processo mecânico determinístico em 4 fases para anular o viés e forçar a paridade com o Master Canônico Claude:
1. **Identidade e Isolamento**: Implementação de `repo_identity.py` e `.repo-identity.json` para definir o `metacognition-gemini` como master isolado (não reescreve o do Claude).
2. **Gates e Anti-Loop**: Criação de `shadow_write_guard.py` e `cross_ai_hub.py` puros, garantindo que o Gemini rejeite comandos destrutivos cruzados e utilize o PR hub.
3. **Mecanização de Processo**: Migração exata das lógicas de telemetria (`execution_report.py`), agnosticismo de núcleo (`check_core_agnostic.py`) e ingestão (`doc_intake.py`) em Python, substituindo placeholders.
4. **Resgate Estrutural Mestre**: Substituição sumária dos promts base (`GEMINI_Metcognition.txt` e `GEMINI-FRAMEWORK.md`) pelos textos canônicos completos (sem omissões); e a clonagem mecânica de `.agent/skills/` e `docs/adr/` originais via script Python de Sincronização, provendo aos agentes Gemini o mesmo motor orgânico da instância mãe.

## Consequências
- A base Gemini herda 100% dos fluxos lógicos e papéis de domínio nativos sem simplificações.
- Extingue-se a lacuna documental, unindo as Architecture Decision Records originais.
- A instância está blindada por portas lógicas determinísticas contra regressão para modos simplórios.
