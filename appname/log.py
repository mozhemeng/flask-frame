import logging
from logging import handlers

from appname.utils.path_utils import PROJECT_ROOT


def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel("INFO")
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')

    file_path = PROJECT_ROOT.joinpath('logs', logger_name+'.log')
    file_handler = handlers.RotatingFileHandler(file_path, maxBytes=20 * 1024 * 1024, backupCount=5)
    file_handler.setLevel("WARNING")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel("INFO")
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger("global_logger")
