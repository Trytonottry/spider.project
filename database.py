# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:01:48 2025

@author: Semyon
"""

# database.py

import sqlite3
import pandas as pd
from logger import logger

def create_database(db_name):
    """Создает базу данных и таблицы, если они не существуют."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                query TEXT,
                data TEXT
            )
        ''')
        conn.commit()
        conn.close()
        logger.info(f"База данных {db_name} создана.")
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}")

def save_to_db(db_name, query, data):
    """Сохраняет результаты поиска в базу данных."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO results (query, data) VALUES (?, ?)", (query, str(data)))
        conn.commit()
        conn.close()
        logger.info(f"Данные сохранены в базу данных: {query}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных: {e}")

def load_external_data(db_name, file_path):
    """Загружает внешние данные (CSV, Excel) в базу данных."""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Неподдерживаемый формат файла. Используйте CSV или Excel.")

        conn = sqlite3.connect(db_name)
        df.to_sql('external_data', conn, if_exists='append', index=False)
        conn.close()
        logger.info(f"Данные из файла {file_path} загружены в базу данных.")
    except Exception as e:
        logger.error(f"Ошибка при загрузке внешних данных: {e}")