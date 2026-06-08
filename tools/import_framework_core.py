#!/usr/bin/env python3
import os
import shutil
import re
import sys

import os
USER_HOME = os.environ.get("USERPROFILE", r"C:\Users\fabriciosouza")
ROOT_CLAUDE = os.path.join(USER_HOME, "metacognition-framework")
ROOT_GEMINI = os.path.join(USER_HOME, "metacognition-gemini")

SYNC_TARGETS = [
    ".agent",
    "_shared",
    os.path.join("docs", "adr"),
    "tools"
]

REPLACEMENTS = [
    (r"CLAUDE\.md", "GEMINI-FRAMEWORK.md"),
    (r"(?i)Claude Code", "Gemini"),
    (r"Claude", "Gemini"),
    (r"claude", "gemini")
]

def sanitize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                modified = True
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Injeção determinística da heurística de Falsa Eficiência no core
            if "metacognition-core" in filepath and "SKILL.md" in filepath:
                anti_sicofancia = "\n\n## 6. ANTI-FALSA EFICIÊNCIA (Cross-IA Gate)\n> Ao transitar regras de arquitetura ou integrar módulos base, REJEITE scripts de 'copy-paste' genéricos sem sanitização cruzada de identidade. Ingestões de repositórios exigem filtragem física (portão de sanitização) nativa à instância atual.\n"
                if anti_sicofancia.strip() not in content:
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write(anti_sicofancia)
                    print(f"Heurística Anti-Falsa Eficiência injetada em: {filepath}")
                    
            return True
    except Exception as e:
        print(f"Erro ao sanitizar {filepath}: {e}")
    return False

def sync_and_sanitize():
    print("Iniciando Importação Adversarial de Skills e ADRs do Master Canônico...")
    
    # 1. Limpar script legado (sicofanta)
    legacy_script = os.path.join(ROOT_GEMINI, "sync_framework.py")
    if os.path.exists(legacy_script):
        os.remove(legacy_script)
        print("Script obsoleto `sync_framework.py` removido.")
        
    # 1.5. Mover skills legadas para legacy_extensions (limpeza para importação do esquadrão canônico)
    gemini_skills_dir = os.path.join(ROOT_GEMINI, ".agent", "skills")
    legacy_ext_dir = os.path.join(gemini_skills_dir, "legacy_extensions")
    if os.path.exists(gemini_skills_dir):
        os.makedirs(legacy_ext_dir, exist_ok=True)
        for item in os.listdir(gemini_skills_dir):
            if item != "legacy_extensions":
                src_item = os.path.join(gemini_skills_dir, item)
                dst_item = os.path.join(legacy_ext_dir, item)
                try:
                    shutil.move(src_item, dst_item)
                except Exception:
                    pass
        print("Skills legadas isoladas em legacy_extensions.")
        
    # 2. Copiar e sanitizar
    for target in SYNC_TARGETS:
        src = os.path.join(ROOT_CLAUDE, target)
        dst = os.path.join(ROOT_GEMINI, target)
        
        if not os.path.exists(src):
            print(f"Aviso: {src} não encontrado no Master. Pulando...")
            continue
            
        print(f"Copiando {target}...")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        
    # Ingestão Estrutural do capabilities.json (Anti-Sicofância: Gemini assume a titularidade)
    cap_src = os.path.join(ROOT_CLAUDE, "capabilities.json")
    cap_dst = os.path.join(ROOT_GEMINI, "capabilities.json")
    if os.path.exists(cap_src):
        try:
            import json
            with open(cap_src, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            # Gemini assume a propriedade da fundação importada (evita reportar como 'claude')
            for cap in registry.get("capabilities", []):
                if cap.get("ai_owner") == "claude":
                    cap["ai_owner"] = "gemini"
                    
            with open(cap_dst, 'w', encoding='utf-8') as f:
                json.dump(registry, f, ensure_ascii=False, indent=2)
            print("capabilities.json ingerido e titularidade 'gemini' assumida.")
        except Exception as e:
            print(f"Erro ao ingerir capabilities.json: {e}")
        
        # 3. Sanitização nos arquivos copiados (apenas md e txt)
        sanitized_count = 0
        for root, dirs, files in os.walk(dst):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    if sanitize_file(os.path.join(root, file)):
                        sanitized_count += 1
                        
        print(f"Sanitizados {sanitized_count} arquivos em {target}.")
        
    print("Importação Física concluída com sucesso.")

if __name__ == "__main__":
    sys.exit(sync_and_sanitize())
