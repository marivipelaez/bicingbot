# -*- coding: utf-8 -*-

u"""
Copyright 2016 Marivi Pelaez Alonso.

This file is part of BicingBot.

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bicingbot.database_conn import DatabaseConnection
from bicingbot.internationalization import tr, get_languages
from bicingbot.telegram_bot import get_bot

logger = logging.getLogger(__name__)

LANGUAGE_SETTING = 'language'
LANGUAGE_CALLBACK = 'lang'


def language_command(chat_id, text):
    """
    Sends language options

    :param chat_id: Telegram chat id
    :param text: command name
    """
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(lang_value, callback_data='{}_{}'.format(LANGUAGE_CALLBACK, lang_key)) for
         lang_key, lang_value in get_languages().items()]])
    get_bot().send_message(chat_id=chat_id, text=tr('language_choose', chat_id), reply_markup=keyboard)


def update_language(chat_id, language, callback_query):
    """
    Updates user language and sends a confirmation notification

    :param chat_id: Telegram chat id
    :param language: selected language
    :param callback_query: callback query
    """
    languages = get_languages()
    if language in languages.keys():
        db_connection = DatabaseConnection()
        db_connection.add_setting(chat_id=chat_id, setting=LANGUAGE_SETTING, value=language)
        db_connection.close()

        message = tr('language_updated', chat_id).format(languages[language])
        get_bot().answer_callback_query(callback_query.id, text=message)
        get_bot().send_message(chat_id=chat_id, text=message)


def get_language(chat_id):
    """
    Retrieves the language configured by the user, if exists. Otherwise, None is returned.
    :param chat_id: Telegram chat id
    :return: chat language
    """
    db_connection = DatabaseConnection()
    language = db_connection.get_setting(chat_id=chat_id, setting=LANGUAGE_SETTING)
    db_connection.close()

    return language
