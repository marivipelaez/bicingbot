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

from app.commands import stations_command, pad_number, compact_address
from app.internationalization import STRINGS

chat_id = '333'


@mock.patch('app.commands.Bicing')
@mock.patch('app.commands.get_bot')
def test_station_command_station(get_bot, Bicing):
    get_bot.return_value = mock.MagicMock()
    Bicing.return_value = mock.MagicMock()

    stations_command(chat_id, '155')

    # Check that get_station has been called
    Bicing().get_station.assert_called_with(155)

    # Check that send message has been called with correct arguments
    get_bot().send_message.assert_called_once()
    _, args = get_bot().send_message.call_args_list[0]
    assert args['chat_id'] == chat_id
    assert args['text'].count('\n') == 1


@mock.patch('app.commands.Bicing')
@mock.patch('app.commands.get_bot')
def test_station_command_group(get_bot, Bicing):
    get_bot.return_value = mock.MagicMock()
    Bicing.return_value = mock.MagicMock()

    stations_command(chat_id, 'casa')

    # Check that 5 stations have been found
    assert Bicing().get_station.call_count == 5

    # Check that send message has been called with correct arguments
    get_bot().send_message.assert_called_once()
    _, args = get_bot().send_message.call_args_list[0]
    assert args['chat_id'] == chat_id
    assert args['text'].count('\n') == 5


@mock.patch('app.commands.Bicing')
@mock.patch('app.commands.get_bot')
def test_station_command_unknown(get_bot, Bicing):
    get_bot.return_value = mock.MagicMock()
    Bicing.return_value = mock.MagicMock()

    stations_command(chat_id, 'unknown')

    # Check that get_station has not been called
    Bicing().get_station.assert_not_called()

    # Check that send message has been called with correct arguments
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['unknown_command'])


def test_pad_number_one_digit():
    assert pad_number('5') == '  5'


def test_pad_number_two_digits():
    assert pad_number('10') == '10'


def test_compact_address_short():
    assert compact_address('Pujades') == 'Pujades'


def test_compact_address_long():
    assert compact_address('Passeig Sant Joan') == 'Passeig Sant J'


def test_compact_address_carrer():
    assert compact_address('Carrer Pujades') == 'Pujades'


def test_compact_address_de():
    assert compact_address('Carrer de Pujades') == 'Pujades'


def test_compact_address_del():
    assert compact_address('Ronda del Mig') == 'Ronda Mig'
