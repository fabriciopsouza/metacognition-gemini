import logging
import os
from datetime import datetime

def setup_logger(log_dir: str):
    """
    Configura e retorna dois loggers simultâneos conforme documentação.
    Log 1 (aplicacao): Eventos gerais e ciclo de vida.
    Log 2 (run): Detalhamento por execução e pipeline.
    """
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Formatadores
    app_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    run_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    # Log 1 - Aplicação
    app_log_path = os.path.join(log_dir, f'aplicacao_{timestamp}.log')
    app_handler = logging.FileHandler(app_log_path, encoding='utf-8')
    app_handler.setFormatter(app_formatter)
    
    app_logger = logging.getLogger('aplicacao')
    app_logger.setLevel(logging.INFO)
    if not app_logger.handlers:
        app_logger.addHandler(app_handler)

    # Log 2 - Run (pipeline e detalhes de processamento)
    run_log_path = os.path.join(log_dir, f'run_{timestamp}.log')
    run_handler = logging.FileHandler(run_log_path, encoding='utf-8')
    run_handler.setFormatter(run_formatter)
    
    run_logger = logging.getLogger('run')
    run_logger.setLevel(logging.DEBUG)
    if not run_logger.handlers:
        run_logger.addHandler(run_handler)
        
    return app_logger, run_logger
