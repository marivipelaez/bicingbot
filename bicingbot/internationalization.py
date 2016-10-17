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
        'Hola, soy BicingBot y te ayudo a conocer el estado de las estaciones del Bicing.',
        ''
    ],
    'help': [
        'Estos son mis comandos:',
        ' /ayuda - muestra esta ayuda',
        ' /nuevogrupo - crea un grupo de estaciones',
        ' NOMBRE_GRUPO - muestra el estado de todas las estaciones del grupo',
        ' NÚMERO_ESTACIÓN - muestra el estado de esa estación',
        ' /grupos - muestra el nombre de todos tus grupos',
    ],
    'language_choose': 'Elige tu idioma',
    'unknown_command': 'Lo siento, no te he entendido. Si necesitas ayuda envíame /ayuda.',
    'station_not_found': '[{}] estación no encontrada',
    'wrong_station': '[{}] ups, algo ha ido mal',
    'newgroup_name': 'Envíame el nombre de tu nuevo grupo',
    'newgroup_stations': 'Envíame cada número de estación en un mensaje y cuando termines, envía /fin',
    'newgroup_created': 'Tu nuevo grupo /{} está listo',
    'newgroup_name_format_error': ('Lo siento, ese nombre no es válido. Puede contener letras, números, guiones bajos '
                                   'y guiones, pero no puede ser un número, ni llamarse igual que ninguno de mis '
                                   'comandos'),
    'newgroup_name_already_existing': ('Ya tienes un grupo con ese nombre\nSi quieres mantenerlo, envía /fin'
                                       '\nPara volver a crearlo, {}'),
    'newgroup_not_created': 'Como no has enviado ninguna estación, no he creado el grupo',
    'newgroup_not_overwrite': 'Vale, no modifico tu grupo /{}',
    'newgroup_unknown_command': ('Lo siento, no es un número de estación válido. Envíame un número correcto o /fin '
                                 'para terminar'),
    'newgroup_number_stations_limit': ('Lo siento, sólo puede haber {} estaciones dentro de un grupo. Envíame /fin '
                                       'para terminar'),
    'newgroup_number_groups_limit': 'Lo siento, ya tienes {} grupos y no puedes crear más',
    'groups_empty': 'Aún no tienes grupos. Para crear uno, envíame /nuevogrupo.'
}

STRINGS['en'] = {
    'welcome': [
        "Hi, I'm BicingBot and I'm here to help you to know the status of Bicing stations.",
        ''
    ],
    'help': [
        'These are my commands:',
        ' /help - shows this message',
        ' /newgroup - creates a stations group',
        ' GROUP_NAME - shows the status of all the stations within this group',
        ' STATION_ID - shows the status of this station',
        ' /groups - shows the name of all your groups',
    ],
    'language_choose': 'Choose your language',
    'unknown_command': "I'm sorry, I don't understand you. Send me /help to get my commands.",
    'station_not_found': '[{}] station not found',
    'wrong_station': '[{}] oops, something went wrong',
    'newgroup_name': 'Send me the name of your new group',
    'newgroup_stations': 'Send me each station number in a separated message and when you are done, send me /end',
    'newgroup_created': 'Your new group /{} is ready',
    'newgroup_name_format_error': ('So sorry, but that name is not valid. It can contain letters, numbers, underscores '
                                   'and dashes, but cannot be a number or have the same value as any of my commands.'),
    'newgroup_name_already_existing': ('You already have a group with that name\nTo keep it as it is, send me /end'
                                       '\nTo create it again, {}'),
    'newgroup_not_created': 'You sent me no stations, so I did not store the group',
    'newgroup_not_overwrite': "Okay, I don't modify your group /{}",
    'newgroup_unknown_command': ('So sorry, this is not a valid station number. Send me a valid number or /end to '
                                 'finish'),
    'newgroup_number_stations_limit': 'So sorry, a group only can contain {} stations. Send me /end to finish',
    'newgroup_number_groups_limit': 'So sorry, you already have {} groups and you cannot create any more',
    'groups_empty': 'You have no groups yet. To create one, send me /newgroup.'
}

DEFAULT_LANGUAGE = 'es'


def tr(string_id, chat_id):
    """
    Get localized string

    :param chat_id: Telegram chat id
    :param string_id: string id
    :return: localized string value
    """
    language = DEFAULT_LANGUAGE
    return STRINGS[language][string_id]


def get_languages():
    """
    Get valid bot languages

    :return: list of languages
    """
    return STRINGS.keys()
