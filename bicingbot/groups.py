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

from bicingbot.database_conn import DatabaseConnection
from bicingbot.internationalization import tr
from bicingbot.telegram_bot import get_bot

logger = logging.getLogger(__name__)

GROUPS_CACHE = {}


def get_group_status(chat_id):
    """
    Get group status and initialize status dictionary if it does not exist

    :param chat_id: Telegram chat id
    :return: group status
    """
    try:
        return GROUPS_CACHE[chat_id]['status']
    except KeyError:
        GROUPS_CACHE[chat_id] = {'status': 0, 'name': None, 'stations': []}
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
    if group_status == 0:
        logger.info('COMMAND /newgroup: chat_id={}'.format(chat_id))
        get_bot().send_message(chat_id=chat_id, text=tr('newgroup_name', chat_id))
        set_group_status(chat_id, 1)
        return
    elif group_status == 1:
        # TODO: check forbidden group names: int, /*, in COMMANDS
        # TODO: check existing group names
        GROUPS_CACHE[chat_id]['name'] = text
        get_bot().send_message(chat_id=chat_id, text=tr('newgroup_stations', chat_id))
        set_group_status(chat_id, 2)
    elif group_status == 2:
        from bicingbot.commands import send_stations_status, COMMANDS_ALIAS
        if text in COMMANDS_ALIAS['end']:
            # TODO allow group modification
            # TODO not to create a new group without stations
            DatabaseConnection().create_group(chat_id=chat_id, name=GROUPS_CACHE[chat_id]['name'],
                                              stations=GROUPS_CACHE[chat_id]['stations'])
            get_bot().send_message(chat_id=chat_id,
                                   text=tr('newgroup_created', chat_id).format(GROUPS_CACHE[chat_id]['name']))
            send_stations_status(chat_id, GROUPS_CACHE[chat_id]['stations'])
            del_group_status(chat_id)
        else:
            # TODO: check integer stations
            GROUPS_CACHE[chat_id]['stations'].append(int(text))
