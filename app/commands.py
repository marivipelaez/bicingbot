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

from telegram.emoji import Emoji

from bicing import Bicing, StationNotFoundError
from telegram_bot import get_bot

logger = logging.getLogger(__name__)

# Temporal hardcoded station groups
STATIONS = {'casa': [153, 154, 339, 165, 166], 'trabajo': [168, 160, 158, 159, 157]}

help_message = [
    'Estos son los comandos que entiendo:',
    ' /help - muestra esta ayuda',
    ' /newgroup - crea un grupo de estaciones de Bicing',
    ' /groups - devuelve el nombre de todos tus grupos',
    ' NOMBRE_GRUPO - devuelve el estado de todas las estaciones del grupo',
    ' NÚMERO_ESTACIÓN - devuelve el estado de esa estación',
]


def start_command(chat_id, text):
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    message = [
        'Hola, soy BicingBot y te ayudo a obtener información de las estaciones del Bicing, aunque aún estoy en desarrollo y los grupos no funcionan :(',
        ''
    ]
    get_bot().send_message(chat_id=chat_id, text='\n'.join(message + help_message))


def help_command(chat_id, text):
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    get_bot().send_message(chat_id=chat_id, text='\n'.join(help_message))


def settings_command(chat_id, text):
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))


def stations_command(chat_id, text):
    try:
        stations = STATIONS[text.lower()]
        logger.info('COMMAND /group {}: chat_id={}'.format(text, chat_id))
    except KeyError:
        try:
            stations = [int(text)]
            logger.info('COMMAND /station {}: chat_id={}'.format(text, chat_id))
        except Exception:
            stations = []
            logger.info('UNKNOWN COMMAND {}: chat_id={}'.format(text, chat_id))
            get_bot().send_message(chat_id=chat_id, text='What? Please, send me a station id')

    stations_status = []
    for station_id in stations:
        try:
            stations_status.append(Bicing().get_station(station_id))
        except StationNotFoundError:
            stations_status.append({'error': '[{}] station not found'.format(station_id)})
        except Exception:
            stations_status.append({'error': '[{}] oops, something went wrong'.format(station_id)})
    if stations_status:
        get_bot().send_message(chat_id=chat_id, text=prepare_stations_status_response(stations_status))


def prepare_stations_status_response(stations):
    """
    Beautify stations status output to be rendered in Telegram

    :param stations: list of stations read from Bicing API
    :return: a str with the complete message
    """
    messages = [Emoji.BICYCLE + ' - ' + Emoji.NO_ENTRY_SIGN]
    for station in stations:
        if 'error' in station:
            messages.append(station['error'])
        else:
            messages.append('{} - {} [{}] {} {}'.format(pad_number(station['bikes']), pad_number(station['slots']),
                                                        station['id'], compact_address(station['streetName']),
                                                        station['streetNumber']))
    return '\n'.join(messages)


def pad_number(num):
    """
    If given number has only one digit, a new string with two spaces in the left is returned. Otherwise, the same
     string is returned.

    :param num: string with an integer
    :return: padded string
    """
    if int(num) < 10:
        return '  ' + num
    return num


def compact_address(address):
    """
    Reduce address length to fit in the message

    :param address: street name
    :return: compacted street name
    """
    MAX_LENGTH = 14
    STOP_WORDS = ['Carrer ', 'de ', 'del ']
    for word in STOP_WORDS:
        address = address.replace(word, '')
    return address[:MAX_LENGTH]
