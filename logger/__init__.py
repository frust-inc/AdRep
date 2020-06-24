import logging
import os
from datetime import datetime


def init_logger(config):
    os.makedirs(config["LOG_PATH"], exist_ok=True)
    log_formatter = logging.Formatter(config["FORMAT"])
    root_logger = logging.getLogger()
    root_logger.setLevel(config["LOG_LEVEL"])

    # file_name = "run_{}.log".format(datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S"))
    # file_handler = logging.FileHandler(os.path.join(config["LOG_PATH"], file_name))
    # file_handler.setFormatter(log_formatter)
    # root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


def get_logger():
    return logging.getLogger()
