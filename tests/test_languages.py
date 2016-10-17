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

from bicingbot.internationalization import STRINGS
from bicingbot.language import language_command

chat_id = '333'


@mock.patch('bicingbot.language.get_bot')
def test_language_command(get_bot):
    get_bot.return_value = mock.MagicMock()

    language_command(chat_id, 'language')

    # Check bot calls and temporal cache
    get_bot().send_message.assert_called_with(chat_id=chat_id, text=STRINGS['es']['language_choose'])
