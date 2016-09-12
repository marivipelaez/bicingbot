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

from bicingbot.groups import group_command, del_group_status, GROUPS_CACHE
from bicingbot.internationalization import STRINGS

chat_id = '333'


@mock.patch('bicingbot.groups.DatabaseConnection')
@mock.patch('bicingbot.groups.get_bot')
def test_group_command_newgroup(get_bot, DatabaseConnection):
    get_bot.return_value = mock.MagicMock()
    DatabaseConnection.return_value = mock.MagicMock()
    del_group_status(chat_id)

    group_command(chat_id, 'newgroup')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_name'])
    assert GROUPS_CACHE[chat_id]['status'] == 1

    group_command(chat_id, 'casa')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_stations'])
    assert GROUPS_CACHE[chat_id]['status'] == 2
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'

    group_command(chat_id, '1')
    group_command(chat_id, '2')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_stations'])
    assert GROUPS_CACHE[chat_id]['status'] == 2
    assert GROUPS_CACHE[chat_id]['name'] == 'casa'
    assert GROUPS_CACHE[chat_id]['stations'] == [1, 2]

    group_command(chat_id, 'end')

    # Check bot and database calls
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['newgroup_created'].format('casa'))
    DatabaseConnection().create_group.assert_called_with(chat_id=chat_id, name='casa', stations=[1, 2])
