#!/usr/bin/env python3
"""
session_orchestrator.py - Gerencia o ciclo de vida e economia de tokens da sessão.
Uso:
  python tools/session_orchestrator.py --next-role <role> --objective "Objetivo concluído"
  python tools/session_orchestrator.py --next-role qa-critic --objective "..." --generator-model "Gemini 2.0 Flash"

Gera um prompt otimizado de handoff com:
- Declaração de identidade obrigatória (GAP-4 / ADR-018 §Heterogeneidade)
- Protocolo QA adversarial steelman→ataque→veredito para qa-critic (ADR-018)
- Postura anti-sycophancy para todos os papéis
"""
import argparse
import os
import sys
import datetime
import subprocess

# Matriz de roteamento de modelos por persona
MODEL_MATRIX = {
    "pmo": "Claude 3.5 Sonnet ou Gemini 1.5 Pro (Foco em Orquestração e Lógica)",
    "architect": "o1/o3-mini ou Gemini 1.5 Pro (Raciocínio profundo e design de software)",
    "discovery": "o1/o3-mini ou Gemini 1.5 Pro (Raciocínio analítico)",
    "developer": "Claude 3.5 Sonnet (Excelente aderência a código e diffs cirúrgicos)",
    "qa-critic": "GPT-4o ou Gemini 1.5 Pro (Isolamento de viés, perfil adversarial forte)",
    "docops": "Claude 3.5 Haiku ou Gemini 1.5 Flash (Velocidade e síntese de documentação)",
    "default": "Modelo de fronteira mais recente disponível no seu ambiente"
}

_IDENTITY_BLOCK = """\

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 DECLARAÇÃO DE IDENTIDADE — preencha ANTES de qualquer análise (ADR-018 §Heterogeneidade)
   Seu modelo: [declare — ex: Gemini 2.0 Flash / Claude 3.5 Sonnet / GPT-4o]
   Sua família: [declare — ex: Gemini / Claude / GPT]
   Papel desta sessão: {role}
   Sessão geradora usou: {generator_model}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ Se sua família == família do gerador: declare explicitamente e reduza confiança no veredito.
"""

_QA_PROTOCOL = """\

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  PROTOCOLO QA ADVERSARIAL — ADR-018 (OBRIGATÓRIO para qa-critic)
1. STEELMAN: reconstrua a versão MAIS FORTE do trabalho recebido.
   Declare o que está demonstravelmente correto. Isso calibra severidade e evita nitpick.
2. ATAQUE (hipótese default = existe bug):
   • Erro de agregação / edge case não coberto
   • Premissa INFERIDA tratada como CONFIRMADA
   • Alucinação de campo ou sintaxe
   • False-PASS: gate que declara mas não enforça
3. VEREDITO BINÁRIO (vocabulário ADR-011):
     APROVADO_LIMPO  —ou—  REPROVADO_REWIND_J<N>
   Não invente terceiro termo. Cite o que sobreviveu ao ataque.
PROIBIDO: concordância passiva, sycophancy.
Concordar APENAS quando logicamente demonstrado no passo 2.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

_POSTURE_NOTE = """\

📌 Postura anti-sycophancy (ADR-018 §Disparo condicional):
• Rotina/alta confiança: validação técnica padrão (não forçar QA pesado).
• Ambíguo / alto-impacto / irreversível: QA reforçado OBRIGATÓRIO.
• Concordar passivamente sem verificação = falha de processo.
"""


def get_ideal_model(role):
    return MODEL_MATRIX.get(role.lower(), MODEL_MATRIX["default"])


def generate_handoff_prompt(role, objective_text, generator_model="[declare o modelo gerador]"):
    model_suggestion = get_ideal_model(role)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    identity = _IDENTITY_BLOCK.format(role=role, generator_model=generator_model)
    qa_section = _QA_PROTOCOL if role.lower() in ("qa-critic", "qa_critic", "qa") else _POSTURE_NOTE

    prompt = (
        f"[METACOGNITION FRAMEWORK - HANDOFF DE SESSÃO OTIMIZADA]\n"
        f"Data: {date_str}\n"
        f"Role/Persona Assumida: {role}\n"
        f"Objetivo Concluído na sessão anterior: {objective_text}\n"
        f"{identity}\n"
        f"INSTRUÇÕES PARA A NOVA SESSÃO:\n"
        f"1. Confirme a inicialização do framework em modo SQUAD (✅ Metacognição Framework Ativo).\n"
        f"2. O papel inicial a ser assumido é: {role}.\n"
        f"3. Analise o contexto recente da pasta `docs/` e `history.md`.\n"
        f"4. Prossiga com as tarefas usando esse estado fresco (sem alucinações de histórico passado longo).\n"
        f"{qa_section}"
    )
    return prompt, model_suggestion


def main():
    parser = argparse.ArgumentParser(description="Orquestrador de Sessão para otimização de Tokens e Modelos")
    parser.add_argument("--next-role", dest="next_role", required=True,
                        help="O próximo papel a assumir (ex: qa-critic, developer)")
    parser.add_argument("--objective", required=True,
                        help="Breve resumo do que foi concluído na sessão que está se encerrando")
    parser.add_argument("--generator-model", dest="generator_model",
                        default="[declare o modelo gerador]",
                        help="Modelo/família que gerou o artefato sendo entregue (para header de heterogeneidade)")
    parser.add_argument("--outdir", default="docs/_private/cross-ai/outbox",
                        help="Diretório de saída para o prompt de handoff")

    args = parser.parse_args()

    prompt, model_suggestion = generate_handoff_prompt(
        args.next_role, args.objective, args.generator_model
    )

    os.makedirs(args.outdir, exist_ok=True)
    out_file = os.path.join(args.outdir, f"NEXT_SESSION_PROMPT_{args.next_role}.txt")

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(prompt)

    # [Fallback A] Injeta o prompt diretamente na área de transferência do Windows
    try:
        process = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(input=prompt.encode("utf-16le"))
        clip_success = True
    except Exception:
        clip_success = False

    print(f"✅ Handoff Prompt gerado com sucesso em: {out_file}")
    if clip_success:
        print("📋 [AUTO-COPY] O prompt foi injetado automaticamente na sua Área de Transferência (Clipboard).")
    print(f"🧠 MODELO SUGERIDO para a nova sessão ({args.next_role}): {model_suggestion}")
    print("\n[INSTRUÇÃO PARA O AGENTE]: Informe ao usuário para:")
    if not clip_success:
        print("1. Copiar o conteúdo do arquivo de handoff gerado.")
    print("1. FECHAR a janela de chat atual imediatamente (para zerar a queima de tokens do histórico).")
    print(f"2. ABRIR uma nova sessão selecionando o modelo sugerido: {model_suggestion}")
    print("3. Colar (CTRL+V) o conteúdo na primeira mensagem do novo chat.")


if __name__ == "__main__":
    sys.exit(main())
