import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DGO_Consolidador')))

from src.dgo_etl.parsers.t4_tmpu import extract_t4
from src.dgo_etl.config_manager import load_config

config = load_config()
input_dir = config.get('Paths', 'InputDirectory', fallback='02_Dados_Entrada')
file_name = config.get('SourceFiles', 'DGO_2026', fallback='DGO-OPER-360_2026_v2.xlsx')

# Resolvendo path absoluto para não depender da pasta atual
base_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(base_dir, input_dir.replace('./', ''), file_name)

try:
    print(f"[QA-Critic] Iniciando validação determinística de T4 em: {filepath}")
    df = extract_t4(filepath, 2026)
    
    # Critério Binário 1: Volumetria
    assert len(df) > 0, "QA FAIL: O DataFrame retornado está vazio."
    
    # Critério Binário 2: Integridade da Chave Primária
    null_siglas = df['Sigla'].isnull().sum()
    assert null_siglas == 0, f"QA FAIL: Encontradas {null_siglas} linhas com Sigla nula/None."
    
    # Critério Binário 3: Padronização
    assert df['Indicador'].iloc[0] == 'T4', "QA FAIL: Coluna Indicador não é T4."
    
    # Critério Binário 4: Teste de Âncora (BABET Jan 2026)
    babet = df[(df['Sigla'].str.upper() == 'BABET') & (df['Mês'].str.lower() == 'jan')]
    assert not babet.empty, "QA FAIL: Âncora BABET Jan não encontrada."
    
    print(f"[QA-Critic] PASS - Todas as {len(df)} linhas extraídas e validadas estruturalmente.")
    print(f"BABET Jan 2026 T4 Resultado: {babet['Resultado'].iloc[0]}")
    sys.exit(0) # PASS
    
except AssertionError as ae:
    print(str(ae))
    sys.exit(1) # FAIL
except Exception as e:
    print(f"[QA-Critic] FAIL - Erro de Execução: {e}")
    sys.exit(1) # FAIL
