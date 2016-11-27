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
        ' /idioma - te permite cambiar el idioma de la conversación'
    ],
    'language': 'Español',
    'language_choose': 'Elige tu idioma',
    'language_updated': 'Has cambiado el idioma a Español',
    'unknown_command': 'Lo siento, no te he entendido. Si necesitas ayuda envíame /ayuda.',
    'station_not_found': '[{}] estación no encontrada',
    'wrong_station': '[{}] ups, algo ha ido mal',
    'newgroup_name': 'Envíame el nombre de tu nuevo grupo',
    'newgroup_stations': 'Envíame cada número de estación en un mensaje y cuando termines, envíame /fin',
    'newgroup_created': 'Tu nuevo grupo /{} está listo',
    'newgroup_name_format_error': ('Lo siento, ese nombre no es válido. Puede contener letras, números, guiones bajos '
                                   'y guiones, pero no puede ser un número, ni llamarse igual que ninguno de mis '
                                   'comandos'),
    'newgroup_name_already_existing': ('Ya tienes un grupo con ese nombre\nSi quieres mantenerlo, envíame /fin'
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
        ' /language - to choose the language of the chat'
    ],
    'language': 'English',
    'language_choose': 'Choose your language',
    'language_updated': 'Your language is now English',
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

STRINGS['ca'] = {
    'welcome': [
        "Hola, sóc BicingBot i t'ajudo a conèixer l'estat de les estacions del Bicing.",
        ''
    ],
    'help': [
        'Aquests són els meus comandaments:',
        ' /ajuda - mostra aquesta ajuda',
        " /nougrup - crea un grup d'estacions",
        " NOM_GRUP - mostra l'estat de totes les estacions del grup",
        " NÚMERO_ESTACIÓ - mostra l'estat d'aquesta estació",
        ' /grups - mostra el nom de tots els teus grups',
        " /idioma - et permet canviar l'idioma de la conversa"
    ],
    'language': 'Català',
    'language_choose': 'Tria el teu idioma',
    'language_updated': "Has canviat l'idioma a Català",
    'unknown_command': "Ho sento, no t'he entès. Si necessites ajuda envia'm /ajuda.",
    'station_not_found': '[{}] estació no trobada',
    'wrong_station': '[{}] ups, alguna cosa ha anat malament',
    'newgroup_name': "Envia'm el nom del teu nou grup",
    'newgroup_stations': "Envia'm cada número d'estació en un missatge i quan acabis, envia'm /fi",
    'newgroup_created': 'El teu nou grup /{} està llest',
    'newgroup_name_format_error': ('Ho sento, aquest nom no es vàlid. Pot contenir lletres, nombres, guions baixos '
                                   'i guions, però no pot ser un nombre, ni dir-se igual que cap dels meus '
                                   'comandaments.'),
    'newgroup_name_already_existing': ("Ja tens un grup amb aquest nom\nSi vols mantenir-lo, envia'm /fi"
                                       '\nPer tornar a crear-lo, {}'),
    'newgroup_not_created': 'Com no has enviat cap estació, no he creat el grup',
    'newgroup_not_overwrite': "D'acord, no modifico el teu grup /{}",
    'newgroup_unknown_command': ("Ho sento, no és un número d'estació vàlid. Envia'm un número correcte o /fi "
                                 "per acabar"),
    'newgroup_number_stations_limit': "Ho sento, només pot haver {} estacions dins d'un grup. Envia'm /fi per acabar",
    'newgroup_number_groups_limit': "Ho sento, ja tens {} grups i no pots crear més",
    'groups_empty': "Encara no tens grups. Per crear-ne un de nou, envia'm /nougrup."
}

DEFAULT_LANGUAGE = 'es'


def tr(string_id, chat_id):
    """
    Get localized string

    :param chat_id: Telegram chat id
    :param string_id: string id
    :return: localized string value
    """
    from bicingbot.language import get_language
    try:
        return STRINGS[get_language(chat_id)][string_id]
    except Exception:
        return STRINGS[DEFAULT_LANGUAGE][string_id]


def get_languages():
    """
    Get valid bot languages

    :return: dict with languages
    """
    return {language_key: values['language'] for language_key, values in STRINGS.items()}
