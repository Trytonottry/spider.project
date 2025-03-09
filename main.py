# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:11:33 2025

@author: Semyon
"""

# main.py

import argparse
from gui import run_gui
from telegram_bot import run_bot
from logger import logger

def main():
    parser = argparse.ArgumentParser(description="Паук - OSINT-программа")
    parser.add_argument('--mode', choices=['bot', 'gui', 'cli'], default='gui', help="Режим работы: bot, gui, cli")
    args = parser.parse_args()

    if args.mode == 'bot':
        logger.info("Запуск Telegram-бота")
        run_bot()
    elif args.mode == 'gui':
        logger.info("Запуск графического интерфейса")
        run_gui()
    elif args.mode == 'cli':
        logger.info("Запуск в консольном режиме")
        # Здесь можно добавить консольный интерфейс
        print("Консольный режим пока не реализован.")

if __name__ == "__main__":
    main()