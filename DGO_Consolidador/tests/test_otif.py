import sys
import os

# Adiciona diretório base ao sys.path para import local
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DGO_Consolidador')))

from src.dgo_etl.parsers.otif import extract_otif

filepath = r'F:\Downloads\DGO-OPER-360\DGO-OPER-360_2026_v2.xlsx'

try:
    print(f"Testando extração OTIF em: {filepath}")
    df = extract_otif(filepath, 2026)
    print(f"Linhas extraídas: {len(df)}")
    if len(df) > 0:
        print("Amostra:")
        print(df.head())
        max_val = df['Resultado'].max()
        print(f"Validação C1c (Max <= 1.0): {max_val} <= 1.0 -> {max_val <= 1.0}")
    else:
        print("Aviso: DataFrame vazio.")
except Exception as e:
    print(f"Falha na validação: {e}")
