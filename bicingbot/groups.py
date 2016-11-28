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
import re

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from bicingbot.database_conn import DatabaseConnection
from bicingbot.internationalization import tr
from bicingbot.telegram_bot import get_bot
from bicingbot.utils import is_integer, grouper

logger = logging.getLogger(__name__)

GROUPS_CACHE = {}
MAX_NUMBER_STATIONS = 20
MAX_NUMBER_GROUPS = 100
GROUP_STATUS_INIT = 0
GROUP_STATUS_NEWGROUP_NAME = 1
GROUP_STATUS_NEWGROUP_STATIONS = 2
REMOVE_GROUP_CALLBACK = 'remove'


def get_group_status(chat_id):
    """
    Get group status and initialize status dictionary if it does not exist

    :param chat_id: Telegram chat id
    :return: group status
    """
    try:
        return GROUPS_CACHE[chat_id]['status']
    except KeyError:
        GROUPS_CACHE[chat_id] = {'status': GROUP_STATUS_INIT, 'name': None, 'stations': []}
        return GROUPS_CACHE[chat_id]['status']


def set_group_status(chat_id, status):
    """
    Set group status value

    :param chat_id: Telegram chat id
    :param status: group status
    """
    GROUPS_CACHE[chat_id]['status'] = status


def del_group_status(chat_id):
    """
    Delete group status

    :param chat_id: Telegram chat id
    """
    try:
        del GROUPS_CACHE[chat_id]
    except KeyError:
        pass


def newgroup_command(chat_id, text):
    """
    Manages the workflow to create a new group.

    :param chat_id: Telegram chat id
    :param text: group command
    """
    group_status = get_group_status(chat_id)
    from bicingbot.commands import send_stations_status, COMMANDS
    db_connection = DatabaseConnection()
    if group_status == GROUP_STATUS_INIT:
        logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
        if len(db_connection.get_groups_names(chat_id)) < MAX_NUMBER_GROUPS:
            get_bot().send_message(chat_id=chat_id, text=tr('newgroup_name', chat_id))
            set_group_status(chat_id, GROUP_STATUS_NEWGROUP_NAME)
        else:
            get_bot().send_message(chat_id=chat_id,
                                   text=tr('newgroup_number_groups_limit', chat_id).format(MAX_NUMBER_GROUPS))
            del_group_status(chat_id)
    elif group_status == GROUP_STATUS_NEWGROUP_NAME:
        if text in COMMANDS['end']['alias']:
            get_bot().send_message(chat_id=chat_id, text=tr('newgroup_not_created', chat_id))
            del_group_status(chat_id)
        elif not is_valid_group_name(text):
            get_bot().send_message(chat_id=chat_id, text=tr('newgroup_name_format_error', chat_id))
        else:
            message = tr('newgroup_stations', chat_id)
            if text in db_connection.get_groups_names(chat_id):
                message = tr('newgroup_name_already_existing', chat_id).format(message.lower())
            GROUPS_CACHE[chat_id]['name'] = text
            get_bot().send_message(chat_id=chat_id, text=message)
            set_group_status(chat_id, GROUP_STATUS_NEWGROUP_STATIONS)
    elif group_status == GROUP_STATUS_NEWGROUP_STATIONS:
        if text in COMMANDS['end']['alias']:
            if GROUPS_CACHE[chat_id]['stations']:
                db_connection.delete_group(chat_id=chat_id, name=GROUPS_CACHE[chat_id]['name'])
                db_connection.create_group(chat_id=chat_id, name=GROUPS_CACHE[chat_id]['name'],
                                           stations=GROUPS_CACHE[chat_id]['stations'])
                get_bot().send_message(chat_id=chat_id,
                                       text=tr('newgroup_created', chat_id).format(GROUPS_CACHE[chat_id]['name']))
                send_stations_status(chat_id, GROUPS_CACHE[chat_id]['stations'])
            else:
                if GROUPS_CACHE[chat_id]['name'] in db_connection.get_groups_names(chat_id):
                    get_bot().send_message(chat_id=chat_id, text=tr('newgroup_not_overwrite', chat_id).format(
                        GROUPS_CACHE[chat_id]['name']))
                else:
                    get_bot().send_message(chat_id=chat_id, text=tr('newgroup_not_created', chat_id))
            del_group_status(chat_id)
        elif is_integer(text):
            if len(GROUPS_CACHE[chat_id]['stations']) < MAX_NUMBER_STATIONS:
                GROUPS_CACHE[chat_id]['stations'].append(int(text))
            else:
                get_bot().send_message(chat_id=chat_id,
                                       text=tr('newgroup_number_stations_limit', chat_id).format(MAX_NUMBER_STATIONS))
        else:
            get_bot().send_message(chat_id=chat_id, text=tr('newgroup_unknown_command', chat_id))

    db_connection.close()


def is_valid_group_name(text):
    """
    Checks if the given text fits into group name format

    :param text: string to validate
    :return: True if the text is a valid group name, False otherwise
    """
    from bicingbot.commands import COMMANDS
    commands_alias = [value for values in COMMANDS.values() for value in values['alias']]
    return re.match("^[\w\d_-]{1,20}$", text) and not is_integer(text) and text not in commands_alias


def remove_group_command(chat_id, text):
    """
    Sends a keyboard to the user with the name of all her groups to choose the one to remove

    :param chat_id: Telegram chat id
    :param text: remove group command
    """
    db_connection = DatabaseConnection()
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    groups = grouper(db_connection.get_groups_names(chat_id))
    buttons_lines = []
    for groups_line in groups:
        buttons_lines.append([InlineKeyboardButton(group_name, callback_data='remove_{}'.format(group_name))
                              for group_name in groups_line if group_name])
    keyboard = InlineKeyboardMarkup(buttons_lines)
    get_bot().send_message(chat_id=chat_id, text=tr('removegroup_name', chat_id), reply_markup=keyboard)
    db_connection.close()


def remove_group(chat_id, group_name, callback_query):
    """
    Removes the group and sends a confirmation notification

    :param chat_id: Telegram chat id
    :param group_name: group name to be removed
    :param callback_query: callback query
    """
    db_connection = DatabaseConnection()
    if group_name not in db_connection.get_groups_names(chat_id):
        get_bot().send_message(chat_id=chat_id, text=tr('removegroup_not_found', chat_id))
    else:
        stations = db_connection.get_group(chat_id, group_name)['stations']
        db_connection.delete_group(chat_id=chat_id, name=group_name)
        message = tr('removegroup_removed', chat_id).format(group_name, ', '.join(str(station) for station in stations))
        get_bot().answer_callback_query(callback_query.id, text=message)
        get_bot().edit_message_text(chat_id=chat_id, text=message, message_id=callback_query.message.message_id)
    db_connection.close()


def groups_command(chat_id, text):
    """
    Sends a message to the user with the name of all her groups

    :param chat_id: Telegram chat id
    :param text: command name
    """
    logger.info('COMMAND {}: chat_id={}'.format(text, chat_id))
    db_connection = DatabaseConnection()
    groups = db_connection.get_groups_names(chat_id)
    db_connection.close()
    if groups:
        get_bot().send_message(chat_id=chat_id, text=', '.join(['/' + group for group in groups]))
    else:
        get_bot().send_message(chat_id=chat_id, text=tr('groups_empty', chat_id))
