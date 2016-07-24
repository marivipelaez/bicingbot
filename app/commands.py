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
from internationalization import tr
from telegram_bot import get_bot

logger = logging.getLogger(__name__)

# Temporal hardcoded station groups
STATIONS = {'casa': [153, 154, 339, 165, 166], 'trabajo': [168, 160, 158, 159, 157]}


def start_command(chat_id, text):
    """
    Sends welcome message to the user

    :param chat_id: Telegram chat id
    :param text: command name
    """
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    get_bot().send_message(chat_id=chat_id, text='\n'.join(tr('welcome', chat_id) + tr('help', chat_id)))


def help_command(chat_id, text):
    """
    Sends help message to the user

    :param chat_id: Telegram chat id
    :param text: command name
    """
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    get_bot().send_message(chat_id=chat_id, text='\n'.join(tr('help', chat_id)))


def settings_command(chat_id, text):
    """
    Sends a message to the user with user settings

    :param chat_id: Telegram chat id
    :param text: command name
    """
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))


def stations_command(chat_id, text):
    """
    Requests the status of a station or a group of stations and sends this message to the user

    :param chat_id: Telegram chat id
    :param text: station id or group name
    """
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
            get_bot().send_message(chat_id=chat_id, text=tr('unknown_command', chat_id))

    stations_status = []
    for station_id in stations:
        try:
            stations_status.append(Bicing().get_station(station_id))
        except StationNotFoundError:
            stations_status.append({'error': tr('station_not_found', chat_id).format(station_id)})
        except Exception:
            stations_status.append({'error': tr('wrong_station', chat_id).format(station_id)})
    if stations_status:
        get_bot().send_message(chat_id=chat_id, text=prepare_stations_status_response(stations_status))


def prepare_stations_status_response(stations):
    """
    Beautifies stations status output to be rendered in Telegram

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
    Reduces address length to fit in the message

    :param address: street name
    :return: compacted street name
    """
    max_length = 14
    stop_words = ['Carrer ', 'de ', 'del ']
    for word in stop_words:
        address = address.replace(word, '')
    return address[:max_length]
