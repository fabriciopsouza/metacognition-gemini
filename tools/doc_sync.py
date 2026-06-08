import hashlib
import json
from pathlib import Path

def hash_file(filepath):
    """Calcula SHA-256 de um arquivo."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def doc_sync(repo_path="."):
    """
    Sincroniza e verifica o status da documentação transversal (ex: AGENTIC_Metcognition.txt)
    entre o master e as instâncias locais.
    """
    repo = Path(repo_path)
    # Procurando a regra na pasta raiz local do hub/framework, se houver
    # Apenas como gate de leitura para validar a desatualização.
    metacognition_path = repo.parent / "metacognition-framework" / "AGENTIC_Metcognition.txt"
    sync_state_file = repo / ".doc_sync_state.json"
    
    if not metacognition_path.exists():
        print(f"AVISO: Documento mestre não localizado em {metacognition_path}")
        return False
        
    current_hash = hash_file(metacognition_path)
    
    saved_hash = None
    if sync_state_file.exists():
        try:
            with open(sync_state_file, 'r', encoding='utf-8') as f:
                saved_hash = json.load(f).get("metacognition_hash")
        except Exception:
            pass
            
    if saved_hash != current_hash:
        print(f"Sincronização necessária! O documento raiz foi alterado.")
        # Salva o novo hash (simulando a sincronia de leitura)
        with open(sync_state_file, 'w', encoding='utf-8') as f:
            json.dump({"metacognition_hash": current_hash}, f, indent=4)
        print("Estado de Doc-Sync atualizado para a versão mais recente da Arquitetura Mental.")
        return True
    else:
        print("Doc-Sync: A documentação local (memória mental) já está sincronizada com a versão root.")
        return True

if __name__ == "__main__":
    doc_sync()
