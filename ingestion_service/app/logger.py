import logging

def setup_logger():
    logger = logging.getLogger('ingestion')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s'
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger
