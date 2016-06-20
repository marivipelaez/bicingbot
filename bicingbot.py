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

from bicing import Bicing, StationNotFoundError

# Initialize Flask app
app = Flask(__name__)

# Initialize logger
app_path = os.path.dirname(os.path.realpath(__file__))
output_log_filename = os.path.join(app_path, 'bicingbot.log').replace('\\', '\\\\')
logging.config.fileConfig(os.path.join(app_path, 'logging.conf'), {'logfilename': output_log_filename}, False)
global logger
logger = logging.getLogger(__name__)
logger.info('Starting BicingBot server')

# Get Telegram token from file
with open(os.path.join(app_path, 'token'), 'rb') as f:
    token = f.readline().decode(encoding='UTF-8').rstrip('\n')

# Get bot instance
global bot
bot = telegram.Bot(token=token)

# Temporal hardcoded station groups
STATIONS = {'casa': [153, 154, 339, 165, 166], 'trabajo': [168, 160, 158, 159, 157]}


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

    :return: HTTP_RESPONSE with 200 OK status and a status message.
    """

    update = telegram.Update.de_json(request.get_json(force=True))
    chat_id = update.message.chat.id
    text = update.message.text

    try:
        stations = STATIONS[text.lower()]
        logger.info('Get group: chat_id={}, text={}'.format(chat_id, text))
    except KeyError:
        try:
            stations = [int(text)]
            logger.info('Get station: chat_id={}, text={}'.format(chat_id, text))
        except Exception:
            stations = []
            logger.info('Unknown command: chat_id={}, text={}'.format(chat_id, text))
            bot.sendMessage(chat_id=chat_id, text='What? Please, send me a station id')

    for station_id in stations:
        try:
            station = Bicing().get_station(station_id)
            resp = '{} bikes, {} slots [{}] {} {}'.format(station['bikes'], station['slots'], station_id,
                                                          station['streetName'], station['streetNumber'])
        except StationNotFoundError:
            resp = '{}: station not found'.format(station_id)
        except Exception:
            resp = '{}: oops, something went wrong'.format(station_id)
        bot.sendMessage(chat_id=chat_id, text=resp)
    return 'Handling your webhook'


@app.route('/setwebhook')
def set_webhook():
    """
    Sets the BicingBot webhook in its Telegram Bot
    :return: HTTP_RESPONSE with 200 OK status and a status message.
    """

    bot_response = bot.setWebhook('{}/bicingbot'.format(request.url_root))
    logger.debug(bot_response)
    return 'Webhook configured'
