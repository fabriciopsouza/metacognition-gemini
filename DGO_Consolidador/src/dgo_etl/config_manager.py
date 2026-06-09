import configparser
import os

def load_config(config_path: str = None) -> configparser.ConfigParser:
    """
    Carrega o arquivo settings.ini evitando hardcodes no código fonte.
    """
    if config_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = os.path.join(base_dir, 'config', 'settings.ini')
        
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {config_path}")
        
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config
