# -*- coding: utf-8 -*-

"""
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

from bicingbot.groups import GROUPS_CACHE, MAX_NUMBER_GROUPS, MAX_NUMBER_STATIONS
from bicingbot.groups import GROUP_STATUS_NEWGROUP_NAME, GROUP_STATUS_NEWGROUP_STATIONS
from bicingbot.groups import newgroup_command, del_group_status, is_valid_group_name, groups_command
from bicingbot.groups import remove_group_command, remove_group, remove_group_cancel
from bicingbot.internationalization import STRINGS
from tests.utils import CallbackQuery

chat_id = '333'


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command(get_bot, DatabaseConnection, Bicing, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []
    Bicing.return_value = mock.MagicMock()
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_NAME

    newgroup_command(chat_id, 'casa')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_stations'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_STATIONS
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'

    newgroup_command(chat_id, '1')
    newgroup_command(chat_id, '2')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_stations'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_STATIONS
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'
    assert GROUPS_CACHE[chat_id]['stations'] == [1, 2]

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='casa')
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa', stations=[1, 2])
    commands_get_bot().send_message.assert_called_once()
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_cancel(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_not_created'])
    DatabaseConnection().create_group.assert_not_called()
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_number_groups_limit(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['casa{}'.format(i) for i in range(MAX_NUMBER_GROUPS)]
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    expected_text = STRINGS['es']['newgroup_number_groups_limit'].format(MAX_NUMBER_GROUPS)
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=expected_text)
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_bad_formatted_name(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check name is number
    newgroup_command(chat_id, '1')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_format_error'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_NAME

    # Check name starts with /
    newgroup_command(chat_id, '/casa')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_format_error'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_NAME

    # Check name is a command
    newgroup_command(chat_id, 'settings')
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name_format_error'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_NAME


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_existing_name_overwrite(get_bot, DatabaseConnection, Bicing, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['casa']
    DatabaseConnection().get_group.return_value = {'chat_id': 333, 'name': 'casa', 'stations': [1, 2, 3]}
    Bicing.return_value = mock.MagicMock()
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check warning message is sent
    newgroup_command(chat_id, 'casa')
    message = STRINGS['es']['newgroup_name_already_existing'].format(STRINGS['es']['newgroup_stations'].lower())
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=message)
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_STATIONS

    newgroup_command(chat_id, '1')
    newgroup_command(chat_id, '2')
    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='casa')
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa', stations=[1, 2])
    commands_get_bot().send_message.assert_called_once()
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_existing_name_cancel(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['casa']
    DatabaseConnection().get_group.return_value = {'chat_id': 333, 'name': 'casa', 'stations': [1, 2, 3]}
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')

    # Check warning message is sent
    newgroup_command(chat_id, 'casa')
    message = STRINGS['es']['newgroup_name_already_existing'].format(STRINGS['es']['newgroup_stations'].lower())
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=message)
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_STATIONS

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id,
                                              text=STRINGS['es']['newgroup_not_overwrite'].format('casa'))
    DatabaseConnection().create_group.assert_not_called()
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_no_stations(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')
    newgroup_command(chat_id, 'casa')
    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_not_created'])
    DatabaseConnection().create_group.assert_not_called()
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_wrong_station(get_bot, DatabaseConnection, Bicing, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []
    Bicing.return_value = mock.MagicMock()
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')
    newgroup_command(chat_id, 'casa')
    newgroup_command(chat_id, '1')

    newgroup_command(chat_id, 'not a number')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_unknown_command'])
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_STATIONS
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'
    assert GROUPS_CACHE[chat_id]['stations'] == [1]

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='casa')
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa', stations=[1])
    commands_get_bot().send_message.assert_called_once()
    assert chat_id not in GROUPS_CACHE


@mock.patch('bicingbot.commands.get_bot')
@mock.patch('bicingbot.commands.Bicing')
@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_newgroup_command_number_stations_limit(get_bot, DatabaseConnection, Bicing, commands_get_bot):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []
    Bicing.return_value = mock.MagicMock()
    commands_get_bot.return_value = mock.MagicMock()
    del_group_status(chat_id)

    newgroup_command(chat_id, 'newgroup')
    newgroup_command(chat_id, 'casa')
    for i in range(MAX_NUMBER_STATIONS):
        newgroup_command(chat_id, str(i))

    newgroup_command(chat_id, '1000')

    # Check bot calls and temporal cache
    expected_text = STRINGS['es']['newgroup_number_stations_limit'].format(MAX_NUMBER_STATIONS)
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=expected_text)
    assert GROUPS_CACHE[chat_id]['status'] == GROUP_STATUS_NEWGROUP_STATIONS
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'
    assert GROUPS_CACHE[chat_id]['stations'] == [i for i in range(MAX_NUMBER_STATIONS)]

    newgroup_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='casa')
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa',
                                                         stations=[i for i in range(MAX_NUMBER_STATIONS)])
    commands_get_bot().send_message.assert_called_once()
    assert chat_id not in GROUPS_CACHE


def test_is_valid_group_name():
    assert is_valid_group_name('casa')
    assert is_valid_group_name('casacasacasacasacasa')
    assert is_valid_group_name('casa_casa')
    assert is_valid_group_name('casa-casa')
    assert is_valid_group_name('casa10')
    assert not is_valid_group_name('1')
    assert not is_valid_group_name('/14')
    assert not is_valid_group_name('casa/casa')
    assert not is_valid_group_name('casa casa')
    assert not is_valid_group_name('casacasacasacasacasac')
    assert not is_valid_group_name('settings')
    assert not is_valid_group_name('fin')
    assert not is_valid_group_name('casa\\casa')
    assert not is_valid_group_name('casa*')
    assert not is_valid_group_name('casa.casa')


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_groups_command(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['group1', 'group2']

    groups_command(chat_id, '/grupos')

    get_bot().send_message.assert_called_with(chat_id=chat_id, text='/group1, /group2')


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_groups_command_empty(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = []

    groups_command(chat_id, '/grupos')

    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['groups_empty'])


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_remove_group_command(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['group1', 'group2']

    remove_group_command(chat_id, 'removegroup')

    # Check bot calls
    get_bot().send_message.assert_called_once()


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_remove_group(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['group1', 'group2']
    DatabaseConnection().get_group.return_value = {'stations': [1, 2]}

    callback_query = CallbackQuery(1, message_id=111)
    remove_group(chat_id, 'group2', callback_query)

    # Check bot calls
    get_bot().answer_callback_query.assert_called_once()
    get_bot().edit_message_text.assert_called_with(chat_id=chat_id,
                                                   text=STRINGS['es']['removegroup_removed'].format('group2', '1, 2'),
                                                   message_id=111)
    DatabaseConnection().delete_group.assert_called_with(chat_id=chat_id, name='group2')


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_remove_group_not_found(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_groups_names.return_value = ['group1', 'group2']

    callback_query = CallbackQuery(1, message_id=111)
    remove_group(chat_id, 'notfound', callback_query)

    # Check bot calls
    get_bot().answer_callback_query.assert_not_called()
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['removegroup_not_found'])
    DatabaseConnection().delete_group.assert_not_called()


@mock.patch('bicingbot.groups.get_bot')
def test_remove_group_cancel(get_bot):
    get_bot.return_value = mock.MagicMock()

    callback_query = CallbackQuery(1, message_id=111)
    remove_group_cancel(chat_id, callback_query)

    # Check bot calls
    get_bot().answer_callback_query.assert_called_once()
    get_bot().edit_message_text.assert_called_with(chat_id=chat_id, text=STRINGS['es']['removegroup_canceled'],
                                                   message_id=111)
