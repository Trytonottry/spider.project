# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:00:19 2025

@author: Semyon
"""

# logger.py

import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(
    filename=config['LOGGING']['LOG_FILE'],
    level=config['LOGGING']['LOG_LEVEL'],
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)