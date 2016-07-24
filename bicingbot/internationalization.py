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

STRINGS = dict()
STRINGS['es'] = {
    'welcome': [
        'Hola, soy BicingBot y te ayudo a obtener información de las estaciones del Bicing.',
        ''
    ],
    'help': [
        'Estos son los comandos que entiendo por ahora:',
        ' /help - muestra esta ayuda',
        ' NÚMERO_ESTACIÓN - devuelve el estado de esa estación',
        '',
        'Pero en poco tiempo espero entender también estos:',
        ' /newgroup - crea un grupo de estaciones',
        ' /groups - devuelve el nombre de todos tus grupos',
        ' NOMBRE_GRUPO - devuelve el estado de todas las estaciones del grupo',
    ],
    'unknown_command': 'Lo siento, no te he entendido. Si necesitas ayuda envíame /help.',
    'station_not_found': '[{}] estación no encontrada',
    'wrong_station': '[{}] ups, algo ha ido mal'
}

STRINGS['en'] = {
    'welcome': [
        "Hi, I'm BicingBot and I'm here to help you getting information of Bicing stations.",
        ''
    ],
    'help': [
        'These are my commands for the moment:',
        ' /help - shows this message',
        ' STATION_ID - shows the status of this station',
        '',
        'But in short I will understand also these:',
        ' /newgroup - creates a stations group',
        ' /groups - shows the name of all your groups',
        ' GROUP_NAME - shows the status of all the stations within this group',
    ],
    'unknown_command': "I'm sorry, I don't understand you. Send me /help to get my commands.",
    'station_not_found': '[{}] station not found',
    'wrong_station': '[{}] oops, something went wrong'
}

DEFAULT_LANGUAGE = 'es'


def tr(string_id, chat_id):
    """
    Get localized string

    :param chat_id: Telegram chat id
    :param string_id: string id
    :return: localized string value
    """
    # TODO: get chat_id language
    language = DEFAULT_LANGUAGE
    return STRINGS[language][string_id]
