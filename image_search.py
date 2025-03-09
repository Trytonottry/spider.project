# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:04:11 2025

@author: Semyon
"""

# image_search.py

import requests
from logger import logger

def search_by_photo(image_path):
    """Поиск по фото через API Search4Faces."""
    try:
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post("https://api.search4faces.com/search", files=files)
            logger.info(f"Поиск по фото выполнен: {image_path}")
            return response.json()
    except Exception as e:
        logger.error(f"Ошибка при поиске по фото: {e}")
        return {"error": str(e)}