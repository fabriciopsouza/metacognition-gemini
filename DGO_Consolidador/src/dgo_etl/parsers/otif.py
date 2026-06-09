import pandas as pd
from src.dgo_etl.excel_utils import iter_excel_sheet

def extract_otif(filepath: str, year: int) -> pd.DataFrame:
    """
    Extrai indicador OTIF (Realizado e Acumulado).
    De-Para: Coluna Sigla na fonte = 'Base' (col 0).
    Meses em colunas: Jan..Dez.
    """
    # Exemplo extração Realizado Mensal
    sheet_name = 'OTIF Relizado Mensal' # Nome exato conforme spec
    try:
        data = iter_excel_sheet(filepath, sheet_name, ['base', 'jan'])
    except ValueError as e:
        # Tenta fallback se aba foi corrigida na fonte
        if sheet_name == 'OTIF Relizado Mensal':
            data = iter_excel_sheet(filepath, 'OTIF Realizado Mensal', ['base', 'jan'])
        else:
            raise e

    df = pd.DataFrame(data)
    
    # Reshape (Melt) de colunas de meses para linhas
    # A primeira coluna é a Base
    base_col = df.columns[0]
    meses_cols = [c for c in df.columns if str(c).lower() in 
                  ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']]
                  
    df_melt = df.melt(id_vars=[base_col], value_vars=meses_cols, var_name='Mês', value_name='Resultado')
    
    df_melt['Indicador'] = 'OTIF'
    df_melt['Tipo Resultado'] = 'Realizado'
    df_melt['Ano'] = year
    df_melt['Sigla'] = df_melt[base_col]
    
    # Tratamento C1c: OTIF fracionário (se > 1, divide por 100 dependendo da fonte/ano)
    # A spec diz que no BD não pode haver valor > 1
    df_melt['Resultado'] = pd.to_numeric(df_melt['Resultado'], errors='coerce')
    df_melt.loc[df_melt['Resultado'] > 1.0, 'Resultado'] = df_melt['Resultado'] / 100.0
    
    # Remove NaN em Resultado
    df_melt = df_melt.dropna(subset=['Resultado'])
    
    return df_melt[['Indicador', 'Tipo Resultado', 'Ano', 'Mês', 'Sigla', 'Resultado']]
