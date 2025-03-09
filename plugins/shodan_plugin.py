# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:06:28 2025

@author: Semyon
"""

# plugins/shodan_plugin.py

import requests
from logger import logger
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def search_shodan(query):
    """Поиск устройств через Shodan."""
    try:
        url = f"https://api.shodan.io/shodan/host/search?key={config['API_KEYS']['SHODAN_API_KEY']}&query={query}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.error(f"Ошибка при поиске в Shodan: {e}")
        return {"error": str(e)}