import logging

def config_logging(level=logging.INFO, format='%(asctime)s - %(levelname)5s - %(name)-20.20s - %(message)s'):
    """
    Config Application level logging (should not be used in modules)
    """
    logging.basicConfig(level=level, format=format)