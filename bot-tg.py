#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import time
import os

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

from google.cloud import dialogflow

import handler_tools
from handler_tools import MyLogsHandler

def echo(bot, update):
    chat_id = bot.message.chat_id
    user_message = bot.message.text
    project_id = os.environ['project_id']
    try:
        bot_answer = handler_tools.detect_intent_texts(project_id, chat_id, user_message, 'ru-RU')
        if bot_answer:
            bot.message.reply_text(bot_answer)
        else:
            bot.message.reply_text('Я тебя не понял \ud83d\ude14')
            tg_bot.send_sticker(chat_id=bot.message.chat_id, sticker='CAACAgQAAxkBAAEDZgABYafruC6ndkrmlOh0CKZBfCVegSEAAsgJAAJT2PhRg6LNy5OG6mIiBA')
    except Exception:
        logger.exception("Проблема при получении и отправке сообщений")

def start(bot, update):
    bot.message.reply_text('Ура! Я живой!')
    bot.message.reply_text('\u263a\ufe0f')

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Бот для общения в Телеграме запущен")

    try:
        telegram_token = os.environ['telegram_token']
        updater = Updater(telegram_token)
        tg_bot = telegram.Bot(telegram_token)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))

        echo_handler = MessageHandler (Filters.text, echo)
        dp.add_handler(echo_handler)

        updater.start_polling()
        updater.idle()

    except Exception:
        logger.exception('Возникла ошибка в боте для общения в Телеграме ↓')
