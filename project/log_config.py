from loguru import logger

def configure_logger():
    logger.remove()
    logger.add(
        'logs/logfile.log',
        format = '{time} {level} {message}',
        level = 'INFO',
        rotation = '1 week',
        compression = 'zip'
    )
    logger.info('logger configured')