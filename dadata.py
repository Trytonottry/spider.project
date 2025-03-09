# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:04:45 2025

@author: Semyon
"""

# dadata.py

import requests
from logger import logger
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def clean_phone(phone):
    """Очищает и проверяет номер телефона с помощью DaData."""
    url = "https://cleaner.dadata.ru/api/v1/clean/phone"
    headers = {
        "Authorization": f"Token {config['API_KEYS']['DADATA_API_KEY']}",
        "X-Secret": config['API_KEYS']['DADATA_SECRET_KEY'],
        "Content-Type": "application/json"
    }
    data = [phone]
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()[0]
    else:
        return {"error": f"Ошибка: {response.status_code}", "details": response.text}