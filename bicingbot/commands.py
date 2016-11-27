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

from bicingbot.bicing import Bicing, StationNotFoundError
from bicingbot.database_conn import DatabaseConnection
from bicingbot.groups import get_group_status, newgroup_command, groups_command
from bicingbot.internationalization import tr
from bicingbot.language import language_command, update_language
from bicingbot.telegram_bot import get_bot
from bicingbot.utils import pad_number, compact_address, normalize_command_name, is_integer

logger = logging.getLogger(__name__)


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


COMMANDS = {
    'start': {'alias': ['start'], 'method': start_command},
    'help': {'alias': ['help', 'ayuda', 'ajuda'], 'method': help_command},
    'settings': {'alias': ['settings'], 'method': settings_command},
    'language': {'alias': ['language', 'idioma'], 'method': language_command},
    'newgroup': {'alias': ['newgroup', 'nuevogrupo', 'nougrup'], 'method': newgroup_command},
    'groups': {'alias': ['groups', 'grupos', 'grups'], 'method': groups_command},
    'end': {'alias': ['end', 'fin', 'fi'], 'method': None}
}


def get_command_method(text):
    """
    If exists, retrieves the method to be executed for that command

    :param text: command to be executed
    :return: the method to be executed or None
    """
    for command in COMMANDS.values():
        if text in command['alias']:
            return command['method']
    return None


def bicingbot_commands(chat_id, text):
    """
    Handles bicingbot specific commands and sends the corresponding messages to the user

    :param chat_id: Telegram chat id
    :param text: command to be executed
    """
    text = normalize_command_name(text)
    command_method = get_command_method(text)
    if get_group_status(chat_id) > 0:
        newgroup_command(chat_id, text)
    elif command_method:
        command_method(chat_id, text)
    elif is_integer(text):
        logger.info('COMMAND /station {}: chat_id={}'.format(text, chat_id))
        send_stations_status(chat_id, [int(text)])
    else:
        db_connection = DatabaseConnection()
        if text in db_connection.get_groups_names(chat_id):
            logger.info('COMMAND /group {}: chat_id={}'.format(text, chat_id))
            group = db_connection.get_group(chat_id, text)
            send_stations_status(chat_id, group['stations'])
        else:
            logger.info('UNKNOWN COMMAND {}: chat_id={}'.format(text, chat_id))
            get_bot().send_message(chat_id=chat_id, text=tr('unknown_command', chat_id))
        db_connection.close()


def send_stations_status(chat_id, stations):
    """
    Sends the status of the given stations to the user

    :param chat_id: Telegram chat id
    :param stations: list of stations identifiers
    """
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


def bicingbot_callback_response(chat_id, callback_query_id, data):
    """
    Handles bicingbot callback query responses and sends the corresponding messages to the user

    :param chat_id: Telegram chat id
    :param callback_query_id: unique callback query id
    :param data: callback query response
    """
    update_language(chat_id, callback_query_id, data)
