import pandas as pd
from src.dgo_etl.excel_utils import iter_excel_sheet

def extract_t4(filepath: str, year: int) -> pd.DataFrame:
    """Extrai indicador T4 (Realizado)."""
    # Apenas 'jan' como âncora, já que 'uos' pode variar (Sigla, N2, etc)
    data = iter_excel_sheet(filepath, 'T4 Realizado', ['jan'])
    df = pd.DataFrame(data)
    
    if df.empty:
        return pd.DataFrame()
        
    meses_str = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    possible_bases = ['uos', 'sigla', 'base', 'unidade', 'n2', 'n3']
    
    base_col = None
    meses_cols = []
    
    for c in df.columns:
        c_lower = str(c).lower().strip()
        is_month = False
        for m in meses_str:
            if m in c_lower:
                meses_cols.append(c)
                is_month = True
                break
        
        if not is_month and base_col is None and any(pb in c_lower for pb in possible_bases):
            base_col = c
            
    if not base_col:
        base_col = df.columns[0]
        
    df_melt = df.melt(id_vars=[base_col], value_vars=meses_cols, var_name='Mês_Raw', value_name='Resultado')
    
    # Padroniza a string do mês removendo emojis ("jan 📋" -> "jan")
    df_melt['Mês'] = df_melt['Mês_Raw'].apply(lambda x: next((m.capitalize() for m in meses_str if m in str(x).lower()), str(x)))
    
    df_melt['Indicador'] = 'T4'
    df_melt['Tipo Resultado'] = 'Realizado'
    df_melt['Ano'] = year
    df_melt['Sigla'] = df_melt[base_col]
    
    df_melt['Resultado'] = pd.to_numeric(df_melt['Resultado'], errors='coerce')
    df_melt = df_melt.dropna(subset=['Resultado'])
    
    return df_melt[['Indicador', 'Tipo Resultado', 'Ano', 'Mês', 'Sigla', 'Resultado']]
