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
from bicingbot.internationalization import tr, get_languages
from bicingbot.telegram_bot import get_bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)


def language_command(chat_id, text):
    """
    Update user language

    :param chat_id: Telegram chat id
    :param text: command name
    """
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    #keyboard = ReplyKeyboardMarkup(get_languages(), one_time_keyboard=True)
    #get_bot().send_message(chat_id=chat_id, text=tr('language_choose', chat_id), reply_markup=keyboard)
    buttons = [[InlineKeyboardButton(lang, callback_data=lang) for lang in get_languages()]]
    keyboard = InlineKeyboardMarkup(buttons)
    get_bot().send_message(chat_id=chat_id, text=tr('language_choose', chat_id), reply_markup=keyboard)
    #get_bot().answerInlineQuery
