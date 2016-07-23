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

import logging.config
import os

import telegram
from flask import Flask, request

from commands import start_command, help_command, settings_command, stations_command
from telegram_bot import get_bot

# Initialize Flask app
app = Flask(__name__)

# Initialize logger
app_path = os.path.dirname(os.path.realpath(__file__))
output_log_filename = os.path.join(app_path, '..', 'bicingbot.log').replace('\\', '\\\\')
config_path = os.path.join(app_path, '..', 'conf')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'), {'logfilename': output_log_filename}, False)
global logger
logger = logging.getLogger(__name__)
logger.info('Starting BicingBot server')

# Telegram bots basic commands
COMMANDS = {
    '/start': start_command,
    '/help': help_command,
    '/settings': settings_command
}


@app.route('/')
def bicingbot_help():
    """
    Welcome point to bicingbot.

    :return: HTTP_RESPONSE with 200 OK status and a welcome message.
    """
    return 'Welcome to BicingBot!'


@app.route('/bicingbot', methods=['GET', 'POST'])
def webhook_handler():
    """
    Handles requests from BicingBot users.
    """
    # Reads request from Telegram user
    update = telegram.Update.de_json(request.get_json(force=True))
    chat_id = update.message.chat.id
    text = update.message.text

    # Checks and runs received command
    try:
        command_method = COMMANDS.get(text)
    except KeyError:
        command_method = stations_command
    command_method(chat_id, text)

    return True


@app.route('/setwebhook')
def set_webhook():
    """
    Sets the BicingBot webhook in its Telegram Bot

    :return: HTTP_RESPONSE with 200 OK status and a status message.
    """
    bot_response = get_bot().setWebhook('{}/bicingbot'.format(request.url_root))
    logger.debug(bot_response)
    return 'Webhook configured'
