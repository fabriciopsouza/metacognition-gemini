import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DGO_Consolidador')))

from src.dgo_etl.parsers.ipar import extract_ipar

filepath = r'F:\Downloads\DGO-OPER-360\DGO-OPER-360_2026_v2.xlsx'

try:
    print(f"Testando extração IPAR em: {filepath}")
    df = extract_ipar(filepath, 2026)
    print(f"Linhas extraídas: {len(df)}")
    if len(df) > 0:
        print("Amostra:")
        print(df.head())
        max_val = df['Resultado'].max()
        print(f"Validação Escala C1 (Max): {max_val}")
        
        # Filtrar BABET Jan
        babet = df[(df['Sigla'].str.upper() == 'BABET') & (df['Mês'].str.lower() == 'jan')]
        if not babet.empty:
            print(f"BABET Jan 2026 Resultado: {babet['Resultado'].iloc[0]}")
    else:
        print("Aviso: DataFrame vazio.")
except Exception as e:
    print(f"Falha na validação: {e}")
