# Gap Analysis: Reconciliação Transacional de PIX

## Contexto de Negócio
A conciliação de final de dia de transações PIX atualmente consome 2 horas da equipe de Controladoria e apresenta falhas silenciosas devido a descompasso de fuso horário em servidores.

## Gap 1: Vazamento de Safra D+1
- **Situação Atual (As Is):** O script de extração puxa dados pelo `timestamp_banco` que está em UTC, comparando com o extrato BACEN que corta em BRT (UTC-3).
- **Ocorrência:** Transações feitas entre 21h00 e 23h59 BRT caem no extrato bancário do dia seguinte na ótica do banco de dados UTC.
- **Risco:** Reporte de saldo negativo falso ao regulador.
- **Solução Proposta (To Be):** Padronizar timezone conversion no script Python antes da junção dos dataframes.

## Gap 2: Tratamento de Webhooks Perdidos
- **Situação Atual (As Is):** Se um PIX entra, o BACEN liquida, mas o webhook do gateway falha (HTTP 500), o banco de dados interno da Fintech não vê o dinheiro.
- **Ocorrência:** R$ 15.000,00 mensais sobram na conta de liquidação sem dono identificado no banco de dados.
- **Risco:** Passivo oculto, dinheiro de cliente bloqueado.
- **Solução Proposta (To Be):** O agente consolidador (framework) deverá identificar o delta `Extrato - BancoDeDados` e acionar uma rotina de *Polling/Retry* via API do gateway usando o EndToEndId para buscar e inserir o registro faltante (Self-healing).

## Gap 3: LGPD Leakage no Logging
- **Situação Atual (As Is):** Os logs em `.txt` das conciliações que falham imprimem a linha inteira, expondo Chaves PIX (CPFs e Telefones).
- **Ocorrência:** Contínua.
- **Risco:** Violação gravíssima LGPD, multa.
- **Solução Proposta (To Be):** Implementar um sanitizador no logger configurado pelo framework. O `logging` passará por um formatter que substitui chaves regex (ex: `[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}`) por `***.***.***-**`.

## Conclusão e Próximos Passos
O fluxo de resolução passa à esteira do framework sob o modo `architect` para formulação do ADR e `developer` para aplicação das restrições de timezone e mascaramento de PII.
