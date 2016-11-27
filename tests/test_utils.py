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

from bicingbot.utils import pad_number, compact_address, normalize_command_name, grouper


def test_normalize_command_name():
    assert 'start' == normalize_command_name('START')
    assert 'start' == normalize_command_name('/start')
    assert 'start' == normalize_command_name('/START')
    assert '' == normalize_command_name('/')
    assert 'start' == normalize_command_name('start')
    assert 'start/' == normalize_command_name('start/')


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


def test_grouper():
    assert list(grouper([1, 2, 3, 4, 5])) == [(1, 2, 3), (4, 5, None)]
