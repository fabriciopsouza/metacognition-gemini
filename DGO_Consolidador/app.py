import streamlit as st
import os
from src.dgo_etl.logger import setup_logger
from src.dgo_etl.config_manager import load_config

# Carrega configurações do .ini
config = load_config()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, config.get('Paths', 'ProcessDirectory', fallback='01_Logs').replace('./', ''))
INPUT_DIR = os.path.join(BASE_DIR, config.get('Paths', 'InputDirectory', fallback='02_Dados_Entrada').replace('./', ''))
OUTPUT_DIR = os.path.join(BASE_DIR, config.get('Paths', 'OutputDirectory', fallback='04_Dados_Integrados').replace('./', ''))

app_logger, run_logger = setup_logger(LOG_DIR)

def main():
    st.title("DGO-OPER-360: Consolidador de Dados (LITE-v2 ESTENDIDO)")
    
    st.sidebar.header("Painel de Controle")
    st.sidebar.markdown(f"**Diretório Base:** `{BASE_DIR}`")
    
    if st.sidebar.button("Executar ETL"):
        st.info("Iniciando rotina de processamento...")
        app_logger.info("Execução manual de ETL acionada pela UI.")
        run_logger.info("Verificando arquivos em 02_Dados_Entrada...")
        
        # O mock da chamada ao pipeline será injetado aqui
        st.warning("Pipeline de ETL em construção.")
        
    st.subheader("Auditoria e Logs")
    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.log')] if os.path.exists(LOG_DIR) else []
    if log_files:
        selected_log = st.selectbox("Visualizar Log:", sorted(log_files, reverse=True))
        with open(os.path.join(LOG_DIR, selected_log), 'r', encoding='utf-8') as f:
            st.text_area("Conteúdo", f.read(), height=300)
    else:
        st.write("Nenhum log disponível.")

if __name__ == "__main__":
    app_logger.info("Aplicação Streamlit iniciada.")
    main()
