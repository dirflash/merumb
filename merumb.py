""" merumb.py """

import os
import sys
import configparser
import logging
from logging import handlers


logger = logging.getLogger("merumb")
logger.setLevel(logging.DEBUG)
logHandler = handlers.RotatingFileHandler(
    r".\logs\debug.log", maxBytes=5600, backupCount=2
)
logHandler.setLevel(logging.DEBUG)
logFormatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
stdHandler = logging.StreamHandler(sys.stdout)
logHandler.setFormatter(logFormatter)
stdHandler.setFormatter(logFormatter)
logger.addHandler(stdHandler)

KEY = "CI"
environ = os.getenv(KEY, default="LOCAL")

if environ == "true":
    mer_key = os.environ["mer_key"]
    mer_org = os.environ["mer_org"]
else:
    config = configparser.ConfigParser()
    config.read("config.ini")
    mer_key = config["MERAKI"]["mer_key"]
    mer_org = config["MERAKI"]["mer_org"]
    logger.addHandler(logHandler)
