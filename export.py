# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:05:57 2025

@author: Semyon
"""

# export.py

import json
import csv
import pandas as pd
from logger import logger

def export_to_json(data, filename):
    """Экспорт данных в JSON."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Данные экспортированы в JSON: {filename}")
    except Exception as e:
        logger.error(f"Ошибка при экспорте в JSON: {e}")

def export_to_csv(data, filename):
    """Экспорт данных в CSV."""
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Результаты"])
            writer.writerow([data])
        logger.info(f"Данные экспортированы в CSV: {filename}")
    except Exception as e:
        logger.error(f"Ошибка при экспорте в CSV: {e}")

def export_to_excel(data, filename):
    """Экспорт данных в Excel."""
    try:
        df = pd.DataFrame({"Результаты": [data]})
        df.to_excel(filename, index=False)
        logger.info(f"Данные экспортированы в Excel: {filename}")
    except Exception as e:
        logger.error(f"Ошибка при экспорте в Excel: {e}")