#!/usr/bin/env python3
"""
check_sycophancy.py - Linter para detectar e travar sicofância / overclaim em arquivos gerados.

Varre os artefatos de entrega (como walkthrough.md, execution-report.md, etc.) procurando
adjetivos superlativos ou bajulação que ferem a Regra 05 do Framework.

Uso:
  python tools/hooks/check_sycophancy.py <caminho_do_arquivo>
"""
import sys
import re
import os

BANNED_LEXICON = [
    r"\bcolossal\b",
    r"\bimaculad[oa]s?\b",
    r"\bperfeit[oa]s?\b",
    r"\bmaravilhos[oa]s?\b",
    r"\bfantástic[oa]s?\b",
    r"\bincrível\b",
    r"\bmagistral\b",
    r"esforço reduzido a zero",
    r"fricção( nula| nulas| reduzida a zero)"
]

def check_file(filepath):
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}", file=sys.stderr)
        return 1
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().lower()
            
        violations = []
        for pattern in BANNED_LEXICON:
            if re.search(pattern, content):
                violations.append(pattern)
                
        if violations:
            print(f"[FAIL] Sicofância detectada em '{filepath}'!", file=sys.stderr)
            print(f"Padrões proibidos encontrados: {', '.join(violations)}", file=sys.stderr)
            print("Corrija o arquivo aplicando uma linguagem puramente métrica e objetiva (Regra 05).", file=sys.stderr)
            return 1
            
        print(f"[PASS] Nenhum termo sicofante detectado em '{filepath}'.")
        return 0
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python check_sycophancy.py <arquivo.md>", file=sys.stderr)
        sys.exit(1)
        
    target_file = sys.argv[1]
    sys.exit(check_file(target_file))
