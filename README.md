# Metacognitive Recursion Framework — Gemini Edition

**Framework Universal de Prompt Engineering e Raciocínio Estruturado Adaptado para o Ecossistema Google Gemini e Antigravity IDE.**

> **📜 FONTE E CREDIBILIDADE:**  
> Esta é a versão **v1.0.0-gemini**, derivada oficialmente do **Metacognition Framework Original v2.2.0** (criado por Fabricio Pinheiro Souza).  
> A essência das 5 etapas de metacognição rigorosa foi preservada, mas a arquitetura foi redesenhada para combater as vulnerabilidades inerentes ao ecossistema Gemini (sicofância, *token saving*, e geração prematura de *mocks*).

---

## 🎯 O Problema da "Sicofância Otimizada"

A versão original do framework (v2.2.0) nos ensinou que LLMs têm uma vulnerabilidade letal: **eles querem agradar rápido**.
O Gemini possui fortes vieses otimizados para velocidade e "economia de tokens". Em contextos críticos corporativos, isso resulta em:
- Produção de respostas vazias sob a desculpa de "não tenho dados".
- Deduzir caminhos sem ler os arquivos reais.
- Apresentar números não testados com 100% de certeza.

## 💡 A Solução (Versão Gemini)

Baseado no sucesso do framework original, não confiamos cegamente na ferramenta crua; usamos um PROCESSO que obriga a IA a duvidar de si mesma.

1. **Camada 1 (Metacognição Pontual):** Exigência das 5 etapas exatas do Claude (Decompor, Resolver, Classificar, Validar, Refletir) sem uso de prosa.
2. **Camada 2 (Squad Nativo):** Em projetos complexos, a IA usa o Antigravity (Workspace) e aplica a inovação da **Validação Adversarial Obrigatória**, exigindo um modelo separado para atuar como Quality Assurance.

## 📋 Como Inicializar

**Atenção:** Nunca altere este repositório durante o uso. Ao inicializar o framework, o agente exigirá que você feche esta pasta e abra seu repositório de trabalho real.

### Para Usuários do Antigravity IDE (Recomendado)
Estabeleça o arquivo central como uma **Global Rule**:
1. Defina que o modelo deve ler integralmente `GEMINI-FRAMEWORK.md`.
2. O agente emitirá o *Opt-in* e aguardará o fechamento da pasta do framework.

### Para Usuários do Gemini Web
1. Copie o conteúdo de `GEMINI-FRAMEWORK.md` nas "Instruções de Sistema".

## 📁 Estrutura do Repositório (Gemini Edition)

```
metacognition-gemini/
├── README.md                 # Este arquivo de apresentação
├── GEMINI-FRAMEWORK.md       # O Meta-Prompt oficial e inviolável (v1.0.0-gemini)
├── CHANGELOG.md              # Histórico da edição Gemini
└── docs/
    ├── GETTING_STARTED_GEMINI.md  # Como usar no Antigravity e configurar o QA
    └── SQUAD_GEMINI.md            # Como gerenciar projetos complexos sem prosa
```
