# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 12:12:49 2025

@author: Semyon
"""

# telegram_bot.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from logger import logger
from configparser import ConfigParser
from search import search_clearnet, search_darknet
from image_search import search_by_photo
from dadata import clean_phone
from plugins.shodan_plugin import search_shodan
from plugins.haveibeenpwned_plugin import check_pwned

config = ConfigParser()
config.read('config.ini')

def start(update: Update, context: CallbackContext):
    """Команда /start."""
    update.message.reply_text('Привет! Я Паук, твой OSINT-помощник.')
    logger.info(f"Пользователь {update.message.from_user.username} начал работу с ботом.")

def search(update: Update, context: CallbackContext):
    """Команда /search."""
    query = ' '.join(context.args)
    results = search_clearnet(query)
    update.message.reply_text('\n'.join(results))

def phone_search(update: Update, context: CallbackContext):
    """Команда /phone."""
    phone = ' '.join(context.args)
    if not phone:
        update.message.reply_text("Укажите номер телефона после команды /phone.")
        return
    result = clean_phone(phone)
    if "error" in result:
        update.message.reply_text(f"Ошибка: {result['error']}")
    else:
        update.message.reply_text(f"Результат:\n{result}")

def email_search(update: Update, context: CallbackContext):
    """Команда /email."""
    email = ' '.join(context.args)
    if not email:
        update.message.reply_text("Укажите email после команды /email.")
        return
    result = check_pwned(email)
    update.message.reply_text(f"Результат:\n{result}")

def run_bot():
    """Запуск бота."""
    try:
        updater = Updater(config['API_KEYS']['TELEGRAM_BOT_TOKEN'])
        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(CommandHandler("search", search))
        updater.dispatcher.add_handler(CommandHandler("phone", phone_search))
        updater.dispatcher.add_handler(CommandHandler("email", email_search))
        updater.start_polling()
        updater.idle()
        logger.info("Telegram-бот запущен.")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")