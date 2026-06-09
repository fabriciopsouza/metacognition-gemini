# Documento de Requisitos: Reconciliação Transacional de PIX (Fintech)

## Identificação do Processo
- **Domínio:** Instituição de Pagamento / Fintech
- **Contexto Regulatório:** Banco Central do Brasil (BACEN), LGPD, PCI-DSS
- **Processo:** Reconciliação Contábil-Financeira de Arranjo de Pagamentos (PIX)
- **Status Atual:** *As Is* (Manual + Scripts Isolados) -> *To Be* (Automação de Reconciliação Determinística)

## Voice of Customer & CTQ (Critical to Quality)
- **Objetivo Central:** Garantir que o saldo consolidado de transações em banco de dados bata no centavo com o saldo liquidado na conta reserva do BACEN ao final do dia (D+0).
- **CTQ (Crítico para Qualidade):** 
  - **Tolerância Zero a Divergência:** O framework deve acusar falha dura se o saldo divergência > R$ 0,00.
  - **Auditabilidade (Audit Trail):** Toda transação conciliada forçadamente ou excluída por regra de negócio deve deixar log rastreável (exigência BACEN).

## Regras de Negócio
1. **Chave de Conciliação:** `ID_Transacao_Interno` + `EndToEndId (E2E) PIX`.
2. **Timezone:** O fechamento diário PIX corta às 23:59:59 (BRT). Fuso horário deve ser explicitamente tratado no código para evitar vazamento D+1.
3. **Casos de Exceção Previstos:**
   - Transação consta no banco de dados mas falhou liquidação no BACEN (estorno pendente).
   - Transação consta no BACEN mas banco de dados perdeu o webhook (timeout de rede).
4. **Proteção de Dados (LGPD/PCI-DSS):** O log do framework *NUNCA* deve imprimir chaves PIX de pessoa física (CPF/Telefone) ou nomes completos. Apenas hashes ou IDs transacionais opacos.

## Classificação pelo Metacognition Framework
- **Regulado:** SIM (BACEN).
- **High-Stakes:** SIM (Decisão executiva / Perda financeira real).
- O `high-stakes-gate` deve estar ATIVO. Edições destrutivas de banco de dados (`DROP`, `UPDATE` massivo) exigem [CONFIRMADO] e fallback/rollback aprovado por HITL (Human-in-the-Loop).
