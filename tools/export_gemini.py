#!/usr/bin/env python3
"""export_gemini.py — Pipeline de EXPORT determinístico de Gemini-Master para Sombras (Premium/Public).

1. Cria árvore limpa copiando o Master.
2. Anônimiza.
3. Carimba `.repo-identity.json` com `role: shadow` e branch target.
Isso impede que Sombras (criadas por este script) jamais atuem como Master-Canônico ou façam
push de volta ao Master. Garantia baseada no ADR-070.
"""
import os
import shutil
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_ROOT = os.path.dirname(HERE)

def strip_pycache(root):
    for dirpath, dirnames, _ in os.walk(root):
        for d in list(dirnames):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, d))
                dirnames.remove(d)

def stamp_shadow_identity(out_root):
    remote = "https://github.com/fabriciopsouza/metacognition-gemini"
    branch, owner = "main", "gemini"
    
    shadow = {
        "schema_version": "1.0",
        "role": "shadow",
        "ai_owner": owner,
        "canonical_remote": remote,
        "canonical_branch": branch,
        "derived_from": "metacognition-gemini (master)",
        "note": "Distribuicao derivada via export_gemini (ADR-049/070). NAO e master; "
                "repo_identity classifica SOMBRA-EXPORT; push e vetado fisicamente."
    }
    with open(os.path.join(out_root, ".repo-identity.json"), "w", encoding="utf-8") as fh:
        json.dump(shadow, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("uso: python tools/export_gemini.py <out-dir>", file=sys.stderr)
        return 2

    out = os.path.abspath(args[0])
    if os.path.abspath(out) == os.path.abspath(SRC_ROOT):
        print("out-dir nao pode ser a propria fonte", file=sys.stderr)
        return 2
    
    if os.path.exists(out):
        shutil.rmtree(out)

    shutil.copytree(SRC_ROOT, out, ignore=shutil.ignore_patterns(".git", "__pycache__", "docs/_private"))
    strip_pycache(out)
    
    stamp_shadow_identity(out)
    print("IDENTITY: .repo-identity.json carimbado role=shadow (ADR-070).")
    print(f"\nEXPORT OK: arvore limpa e shadow-carimbada em {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
