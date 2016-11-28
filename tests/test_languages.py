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

from bicingbot.language import language_command, update_language, get_language, LANGUAGE_SETTING
from tests.utils import CallbackQuery

chat_id = '333'


@mock.patch('bicingbot.language.DatabaseConnection')
@mock.patch('bicingbot.language.get_bot')
def test_language_command(get_bot, DatabaseConnection):
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_setting.return_value = 'en'
    get_bot.return_value = mock.MagicMock()

    language_command(chat_id, 'language')

    # Check bot calls
    get_bot().send_message.assert_called_once()


@mock.patch('bicingbot.language.DatabaseConnection')
@mock.patch('bicingbot.language.get_bot')
def test_update_language(get_bot, DatabaseConnection):
    DatabaseConnection.return_value = mock.MagicMock()
    get_bot.return_value = mock.MagicMock()

    callback_query = CallbackQuery(1)
    update_language(chat_id, 'es', callback_query)

    # Check bot calls
    get_bot().answer_callback_query.assert_called_once()
    get_bot().send_message.assert_called_once()
    DatabaseConnection().add_setting.assert_called_with(chat_id=chat_id, setting=LANGUAGE_SETTING, value='es')


@mock.patch('bicingbot.language.DatabaseConnection')
@mock.patch('bicingbot.language.get_bot')
def test_update_language_wrong(get_bot, DatabaseConnection):
    DatabaseConnection.return_value = mock.MagicMock()
    get_bot.return_value = mock.MagicMock()

    callback_query = CallbackQuery(1)
    update_language(chat_id, 'nolanguage', callback_query)

    # Check bot calls
    get_bot().answer_callback_query.assert_not_called()
    get_bot().send_message.assert_not_called()
    DatabaseConnection().add_setting.assert_not_called()


@mock.patch('bicingbot.language.DatabaseConnection')
def test_get_language(DatabaseConnection):
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_setting.return_value = 'en'

    assert get_language(chat_id) == 'en'


@mock.patch('bicingbot.language.DatabaseConnection')
def test_get_language_wrong(DatabaseConnection):
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_setting.return_value = None

    assert get_language(chat_id) is None
