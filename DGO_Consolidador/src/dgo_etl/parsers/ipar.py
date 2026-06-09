import pandas as pd
from src.dgo_etl.excel_utils import iter_excel_sheet

def extract_ipar(filepath: str, year: int) -> pd.DataFrame:
    """
    Extrai indicador IPAR (Realizado e Acumulado).
    De-Para: Coluna Sigla na fonte = 'Sigla' (col 0).
    Meses em colunas: Jan..Dez.
    """
    sheet_name = 'IPAR Relizado Mensal' # Conforme tabela do documento
    try:
        data = iter_excel_sheet(filepath, sheet_name, ['sigla', 'jan'])
    except ValueError as e:
        if sheet_name == 'IPAR Relizado Mensal':
            data = iter_excel_sheet(filepath, 'IPAR Realizado Mensal', ['sigla', 'jan'])
        else:
            raise e

    df = pd.DataFrame(data)
    
    base_col = df.columns[0]
    meses_cols = [c for c in df.columns if str(c).lower() in 
                  ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']]
                  
    df_melt = df.melt(id_vars=[base_col], value_vars=meses_cols, var_name='Mês', value_name='Resultado')
    
    df_melt['Indicador'] = 'IPAR'
    df_melt['Tipo Resultado'] = 'Realizado'
    df_melt['Ano'] = year
    df_melt['Sigla'] = df_melt[base_col]
    
    df_melt['Resultado'] = pd.to_numeric(df_melt['Resultado'], errors='coerce')
    df_melt = df_melt.dropna(subset=['Resultado'])
    
    # Tratamento C1: IPAR escala 0-100. Se max <= 1.0, multiplicar por 100
    if not df_melt.empty and df_melt['Resultado'].max() <= 1.0:
        df_melt['Resultado'] = df_melt['Resultado'] * 100.0
        
    return df_melt[['Indicador', 'Tipo Resultado', 'Ano', 'Mês', 'Sigla', 'Resultado']]
