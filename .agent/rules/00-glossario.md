# Glossário e Regras de Negócio
# Arquivo base de governança do repositório local

Este arquivo garante que o Agente não invente termos de banco de dados ou regras matemáticas fora do contexto da sua empresa.

- **UsuarioId:** Usar UUID v4. Jamais INT.
- **Status de Pagamento:** Somente `PENDING`, `PAID`, `FAILED`. Não invente `APPROVED`.
- **Valores:** Sempre calculados com precisão de 2 casas decimais.
