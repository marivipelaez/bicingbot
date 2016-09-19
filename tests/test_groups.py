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

import mock

from bicingbot.groups import newgroup_command, del_group_status, GROUPS_CACHE, is_valid_group_name
from bicingbot.internationalization import STRINGS

chat_id = '333'


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_newgroup(get_bot, DatabaseConnection, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_group.return_value = None
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name'])
    assert GROUPS_CACHE[chat_id]['status'] == 1

    newgroup_command(chat_id, 'casa')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_stations'])
    assert GROUPS_CACHE[chat_id]['status'] == 2
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'

    newgroup_command(chat_id, '1')
    newgroup_command(chat_id, '2')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_stations'])
    assert GROUPS_CACHE[chat_id]['status'] == 2
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'
    assert GROUPS_CACHE[chat_id]['stations'] == [1, 2]

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='casa')
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa', stations=[1, 2])
    commands_get_bot().send_message.assert_called_once()


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_newgroup_bad_formatted_name(get_bot, DatabaseConnection, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check name is number
    newgroup_command(chat_id, '1')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_format_error'])
    assert GROUPS_CACHE[chat_id]['status'] == 1

    # Check name starts with /
    newgroup_command(chat_id, '/casa')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_format_error'])
    assert GROUPS_CACHE[chat_id]['status'] == 1

    # Check name is a command
    newgroup_command(chat_id, 'settings')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_format_error'])
    assert GROUPS_CACHE[chat_id]['status'] == 1


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_newgroup_existing_name_overwrite(get_bot, DatabaseConnection, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_group.return_value = {'chat_id': 333, 'name': 'test_group', 'stations': [1, 2, 3]}
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check warning message is sent
    newgroup_command(chat_id, 'casa')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_already_existing'])
    assert GROUPS_CACHE[chat_id]['status'] == 2

    newgroup_command(chat_id, '1')
    newgroup_command(chat_id, '2')
    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='casa')
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa', stations=[1, 2])
    commands_get_bot().send_message.assert_called_once()


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_newgroup_existing_name_cancel(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_group.return_value = {'chat_id': 333, 'name': 'test_group', 'stations': [1, 2, 3]}
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check warning message is sent
    newgroup_command(chat_id, 'casa')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_already_existing'])
    assert GROUPS_CACHE[chat_id]['status'] == 2

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_not_created'])
    DatabaseConnection().create_group.assert_not_called()


def test_is_valid_group_name():
    assert is_valid_group_name('casa')
    assert is_valid_group_name('casacasacasacasacasa')
    assert is_valid_group_name('0.5')
    assert not is_valid_group_name('1')
    assert not is_valid_group_name('/14')
    assert not is_valid_group_name('casa/paco')
    assert not is_valid_group_name('casa paco')
    assert not is_valid_group_name('casacasacasacasacasac')
    assert not is_valid_group_name('settings')
    assert not is_valid_group_name('fin')
