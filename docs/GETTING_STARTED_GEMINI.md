# Como Inicializar o Metacognition Gemini

**Tempo estimado:** 5 minutos.
*Versão do documento: v1.0.0-gemini (Derivada das práticas de Getting Started do repositório original v2.2.0).*

Este guia orienta o setup focado na premissa anti-prosa e na validação adversarial.

## 1. Antigravity IDE (Modo Automático Recomendado)

Se você utiliza o Antigravity IDE, o framework funcionará melhor como uma regra residente:

1. Vá em `Customizations -> Rules -> Global`.
2. Adicione a seguinte instrução fundacional:
   ```
   Eu sou um agente protegido pelo Metacognition Gemini v1.0.0, arquitetura baseada no framework original v2.2.0.
   Ação OBRIGATÓRIA inicial silenciosa: Ler o arquivo GEMINI-FRAMEWORK.md do repositório local e executar o Protocolo de Inicialização (Opt-in).
   Aguardar o fechamento da pasta atual para atuar estritamente em processos anti-sicofância, estruturação sem prosa e gatilhos de Ownership.
   ```

## 2. Autenticação e Autonomia do Agente (Novo Padrão)

Para que o Agente Gemini tenha poder de criar repositórios e executar *commits* para você sem esbarrar em bloqueios do sistema, você precisa fornecer as "chaves do carro" de forma segura.

1. Acesse o GitHub: [Fine-grained Personal Access Tokens](https://github.com/settings/tokens?type=beta)
2. Gere um novo token com permissões de **Administration** e **Contents** (Read and Write).
3. Na raiz deste repositório, faça uma cópia do arquivo `.env.example` e renomeie para `.env`.
4. Cole o seu token: `GITHUB_TOKEN=ghp_sua_chave_aqui`

> [!WARNING]
> O arquivo `.gitignore` do repositório já está configurado para **NUNCA** enviar o arquivo `.env` para a nuvem. Jamais apague o `.gitignore`.

## 3. Configurando a Validação Adversarial (QA)

A pedra angular deste framework (ausente na versão de Claude, exclusiva desta adaptação Gemini) é não permitir que a IA julgue seu próprio trabalho. Se a IA cometer um erro por sicofância, ela será cega à própria falha.

**Fluxo de Execução:**
1. Execute a *feature* usando o modelo principal (Ex: Gemini 1.5 Pro).
2. Ao terminar a criação, congele o desenvolvimento.
3. Chame um sub-agente explicitamente roteado para outro modelo (Ex: Gemini 1.5 Flash).
4. Consulte as regras do papel de QA descritas em `docs/SQUAD_GEMINI.md`. Instrua o modelo atacante: *"Aja como QA Adversarial. Seu único objetivo é tentar encontrar onde a lógica matemática quebra"*.

## 3. Workflow Orientado a Artefatos (Adeus Prosa)

Para manter a integridade que o framework original (v2.2.0) estabeleceu:
- **Não discuta requisitos no fluxo livre da conversa**. 
- Gere arquivos `implementation_plan.md`.
- Permita a ocorrência do *Fail-Fast*. Se o agente pedir para você especificar dados faltantes, atenda à requisição antes de exigir a saída.
