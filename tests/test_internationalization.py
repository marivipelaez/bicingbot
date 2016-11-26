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

from bicingbot.internationalization import tr, STRINGS, get_languages
import mock


@mock.patch('bicingbot.language.DatabaseConnection')
def test_translate_language(DatabaseConnection):
    DatabaseConnection.return_value = mock.MagicMock()
    DatabaseConnection().get_setting.return_value = 'en'

    assert tr('wrong_station', 1) == STRINGS['en']['wrong_station']


def test_translate_default_language():
    assert tr('wrong_station', 1) == STRINGS['es']['wrong_station']


def test_get_languages():
    assert get_languages() == {'en': 'English', 'es': 'Español'}
