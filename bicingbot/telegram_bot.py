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

import os

import telegram

_bot = None


def initialize_bot():
    """
    Reads token and gets new instance of Telegram bot
    """
    # Get Telegram token from file
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'conf')
    with open(os.path.join(config_path, 'token'), 'rb') as f:
        token = f.readline().decode(encoding='UTF-8').rstrip('\n')

    # Get bot instance
    global _bot
    _bot = telegram.Bot(token=token)


def get_bot():
    """
    Gets the already instantiated Telegram client

    :return: Telegram client instance
    :rtype: telegram.Bot
    """
    if not _bot:
        initialize_bot()
    return _bot
