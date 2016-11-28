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

from bicingbot import groups
from bicingbot.commands import bicingbot_commands, bicingbot_callback, COMMANDS
from bicingbot.groups import REMOVE_GROUP_CALLBACK
from bicingbot.internationalization import STRINGS
from bicingbot.language import LANGUAGE_CALLBACK
from tests.utils import CallbackQuery

chat_id = '333'


def test_bicingbot_command_language():
    COMMANDS['language']['method'] = mock.MagicMock()
    bicingbot_commands(chat_id, 'language')
    COMMANDS['language']['method'].assert_called_with(chat_id, 'language')


def test_bicingbot_command_groups():
    COMMANDS['groups']['method'] = mock.MagicMock()
    bicingbot_commands(chat_id, 'groups')
    COMMANDS['groups']['method'].assert_called_with(chat_id, 'groups')


def test_bicingbot_command_newgroup():
    COMMANDS['newgroup']['method'] = mock.MagicMock()
    bicingbot_commands(chat_id, 'newgroup')
    COMMANDS['newgroup']['method'].assert_called_with(chat_id, 'newgroup')


@mock.patch('bicingbot.commands.newgroup_command')
def test_bicingbot_command_newgroup_name(newgroup_command):
    groups.GROUPS_CACHE[chat_id] = {'status': 1, 'name': None, 'stations': []}
    bicingbot_commands(chat_id, 'casa')
    newgroup_command.assert_called_with(chat_id, 'casa')
    del groups.GROUPS_CACHE[chat_id]


@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.commands.get_bot')
def test_bicingbot_command_station(get_bot, Bicing):
    get_bot.return_value = mock.MagicMock()
    Bicing.return_value = mock.MagicMock()

    bicingbot_commands(chat_id, '155')

    # Check that get_station has been called
    Bicing().get_station.assert_called_with(155)

    # Check that send message has been called with correct arguments
    get_bot().send_message.assert_called_once()
    _, args = get_bot().send_message.call_args_list[0]
    assert args['chat_id'] == chat_id
    assert args['text'].count('\n') == 1


@mock.patch('bicingbot.commands.DatabaseConnection')
@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.commands.get_bot')
def test_bicingbot_command_group(get_bot, Bicing, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    Bicing.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['casa']
    DatabaseConnection().get_group.return_value = {'chat_id': chat_id,
                                                   'name': 'casa',
                                                   'stations': [153, 154, 339, 165, 166]}

    bicingbot_commands(chat_id, 'casa')

    # Check that 5 stations have been found
    assert Bicing().get_station.call_count == 5

    # Check that send message has been called with correct arguments
    get_bot().send_message.assert_called_once()
    _, args = get_bot().send_message.call_args_list[0]
    assert args['chat_id'] == chat_id
    assert args['text'].count('\n') == 5


@mock.patch('bicingbot.commands.DatabaseConnection')
@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.commands.get_bot')
def test_bicingbot_command_unknown(get_bot, Bicing, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    Bicing.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []

    bicingbot_commands(chat_id, 'unknown')

    # Check that get_station has not been called
    Bicing().get_station.assert_not_called()

    # Check that send message has been called with correct arguments
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['unknown_command'])


@mock.patch('bicingbot.commands.update_language')
def test_bicingbot_callback_language(update_language):
    update_language.return_value = mock.MagicMock()
    callback_query = CallbackQuery(1)
    bicingbot_callback(chat_id, '{}_en'.format(LANGUAGE_CALLBACK), callback_query)

    # Check that send message has been called with correct arguments
    update_language.assert_called_with(chat_id, 'en', callback_query)


@mock.patch('bicingbot.commands.remove_group')
def test_bicingbot_callback_remove_group(remove_group):
    remove_group.return_value = mock.MagicMock()
    callback_query = CallbackQuery(1, message_id=111)
    bicingbot_callback(chat_id, '{}_group1'.format(REMOVE_GROUP_CALLBACK), callback_query)

    # Check that send message has been called with correct arguments
    remove_group.assert_called_with(chat_id, 'group1', callback_query)


@mock.patch('bicingbot.commands.remove_group')
def test_bicingbot_callback_remove_group_underscore(remove_group):
    remove_group.return_value = mock.MagicMock()
    callback_query = CallbackQuery(1, message_id=111)
    bicingbot_callback(chat_id, '{}_name_group1'.format(REMOVE_GROUP_CALLBACK), callback_query)

    # Check that send message has been called with correct arguments
    remove_group.assert_called_with(chat_id, 'name_group1', callback_query)


@mock.patch('bicingbot.commands.update_language')
@mock.patch('bicingbot.commands.remove_group')
def test_bicingbot_callback_unknown(remove_group, update_language):
    update_language.return_value = mock.MagicMock()
    remove_group.return_value = mock.MagicMock()
    callback_query = CallbackQuery(1)
    bicingbot_callback(chat_id, 'unknown_group1', callback_query)

    # Check that send message has been called with correct arguments
    update_language.assert_not_called()
    remove_group.assert_not_called()
