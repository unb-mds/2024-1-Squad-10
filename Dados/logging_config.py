import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO,
                        filename='info.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configuração de um logger específico (opcional)
    logger = logging.getLogger('logger_coletaAPI')
    logger.setLevel(logging.DEBUG)
    
    # Handler para console (opcional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger

    def setup_logger_01():
    logging.basicConfig(level=logging.INFO,
                        filename='info_erros.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configuração de um logger específico (opcional)
    logger = logging.getLogger('logger_coleta_erros')
    logger.setLevel(logging.DEBUG)
    
    # Handler para console (opcional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger
