#!/usr/bin/env python3
"""effect_gate.py — Intérprete Python da política effect-rules.json (ADR-039).

Uso CLI:
    python tools/effect_gate.py "git reset --hard HEAD"
    python tools/effect_gate.py "rm -rf /"

Saída:
    ALLOW  (benigno — sem regra correspondente)
    ASK    [<id> T2] <motivo>
    DENY   [<id> T3] <motivo>

Exit codes: 0=allow, 1=deny, 2=ask

Uso programático:
    from tools.effect_gate import check_command
    decision, rule = check_command("rm -rf /")
    # decision in {"allow", "ask", "deny"}; rule=None quando allow
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(ROOT, "tools", "effect-rules.json")

_EXIT = {"allow": 0, "deny": 1, "ask": 2}


def load_rules(path=RULES_PATH):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["rules"]


def check_command(cmd: str, rules=None):
    """Avalia `cmd` contra as regras da política.

    Retorna (decision, rule | None).
    decision ∈ {"allow", "ask", "deny"}.
    Ordem: primeira regra que casar vence (política conservadora default-allow).
    """
    if rules is None:
        rules = load_rules()
    low = cmd.lower()
    for rule in rules:
        all_match = all(re.search(p, low) for p in rule["all"])
        if not all_match:
            continue
        none_block = any(re.search(p, low) for p in rule.get("none", []))
        if none_block:
            continue
        return rule["decision"], rule
    return "allow", None


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Uso: python tools/effect_gate.py \"<comando>\"", file=sys.stderr)
        return 2
    cmd = " ".join(argv)
    decision, rule = check_command(cmd)
    if rule:
        tier = rule.get("tier", "T?")
        print(f"{decision.upper()} [{rule['id']} {tier}] {rule['reason']}")
    else:
        print("ALLOW (benigno — sem regra correspondente)")
    return _EXIT.get(decision, 0)


if __name__ == "__main__":
    sys.exit(main())
