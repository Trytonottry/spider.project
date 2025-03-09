# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:07:52 2025

@author: Semyon
"""

# plugins/haveibeenpwned_plugin.py

import requests
from logger import logger
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def check_pwned(email):
    """Проверка email через Have I Been Pwned."""
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {"hibp-api-key": config['API_KEYS']['HAVEIBEENPWNED_API_KEY']}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        logger.error(f"Ошибка при проверке email: {e}")
        return {"error": str(e)}