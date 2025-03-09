# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:03:02 2025

@author: Semyon
"""

# search.py

import requests
from bs4 import BeautifulSoup
from logger import logger
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

def search_clearnet(query):
    """Поиск в клирнете (Google)."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Парсинг результатов
        results = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            title = g.find('h3')
            if title:
                results.append(title.text)
        
        logger.info(f"Поиск в клирнете выполнен: {query}")
        return results if results else ["Ничего не найдено."]
    except Exception as e:
        logger.error(f"Ошибка при поиске в клирнете: {e}")
        return ["Ошибка при поиске в клирнете."]

def search_darknet(query):
    """Поиск в даркнете (через Tor)."""
    try:
        # Используем прокси Tor
        proxies = {
            'http': config['TOR']['TOR_PROXY_HTTP'],
            'https': config['TOR']['TOR_PROXY_HTTPS']
        }

        # Пример реального .onion-сайта (например, DuckDuckGo)
        url = f"http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/?q={query}"
        response = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Парсинг результатов (пример для DuckDuckGo)
        results = []
        for result in soup.find_all('h2', class_='result__title'):
            results.append(result.text.strip())
        
        logger.info(f"Поиск в даркнете выполнен: {query}")
        return results if results else ["Ничего не найдено."]
    except Exception as e:
        logger.error(f"Ошибка при поиске в даркнете: {e}")
        return ["Ошибка при поиске в даркнете."]