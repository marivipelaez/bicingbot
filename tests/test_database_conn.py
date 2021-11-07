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

import pytest

from bicingbot.database_conn import DatabaseConnection
from bicingbot.database_migration import DatabaseMigration
from sqlite3.dbapi2 import IntegrityError

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'tests', 'conf')


@pytest.fixture()
def database_connection():
    os.makedirs(config_path, exist_ok=True)
    try:
        os.remove(os.path.join(config_path, 'bicingbot_test.db'))
    except OSError:
        pass
    DatabaseMigration(database='bicingbot_test.db', config_path=config_path).create_schema()
    conn = DatabaseConnection(database='bicingbot_test.db', config_path=config_path)
    yield conn
    conn.close()


@pytest.fixture()
def check_connection():
    conn = DatabaseConnection(database='bicingbot_test.db', config_path=config_path)
    yield conn
    conn.close()


def test_create_group(database_connection, check_connection):
    database_connection.create_group(chat_id=1, name='test_group', stations=[1, 2, 3])

    cursor = check_connection.connection.cursor()
    rows = cursor.execute('SELECT * FROM groups').fetchall()
    assert len(rows) == 3
    assert rows[0][:3] == (1, 'test_group', 1)
    assert rows[1][:3] == (1, 'test_group', 2)
    assert rows[2][:3] == (1, 'test_group', 3)
    assert rows[0][3] is not None
    assert rows[0][3] == rows[1][3]
    assert rows[0][3] == rows[2][3]


def test_create_group_existent(database_connection, check_connection):
    with pytest.raises(IntegrityError):
        database_connection.create_group(chat_id=1, name='test_group', stations=[1, 1, 3])

    cursor = check_connection.connection.cursor()
    rows = cursor.execute('SELECT * FROM groups').fetchall()
    assert len(rows) == 0


def test_get_group(database_connection):
    database_connection.create_group(chat_id=1, name='test_group', stations=[1, 2, 3])
    database_connection.create_group(chat_id=2, name='test_group', stations=[1, 2, 3])
    group = database_connection.get_group(1, 'test_group')

    assert group == {'chat_id': 1, 'name': 'test_group', 'stations': [1, 2, 3]}


def test_get_group_nonexisting(database_connection):
    group = database_connection.get_group(1, 'test_group')

    assert group is None


def test_get_groups_names(database_connection):
    database_connection.create_group(chat_id=1, name='test_group', stations=[1, 2, 3])
    database_connection.create_group(chat_id=1, name='test_group2', stations=[1, 2, 3])
    database_connection.create_group(chat_id=2, name='test_group', stations=[1, 2, 3])
    groups_names = database_connection.get_groups_names(1)

    assert groups_names == ['test_group', 'test_group2']


def test_delete_group(database_connection, check_connection):
    database_connection.create_group(chat_id=1, name='test_group', stations=[1, 2, 3])
    database_connection.delete_group(1, 'test_group')

    cursor = check_connection.connection.cursor()
    rows = cursor.execute('SELECT * FROM groups').fetchall()
    assert len(rows) == 0


def test_delete_group_nonexisting(database_connection):
    database_connection.delete_group(1, 'test_group')


def test_add_setting(database_connection, check_connection):
    database_connection.add_setting(chat_id=1, setting='language', value='es')

    cursor = check_connection.connection.cursor()
    rows = cursor.execute('SELECT * FROM settings where chat_id=1').fetchall()
    assert len(rows) == 1
    assert rows[0][:3] == (1, 'language', 'es')


def test_add_setting_existent(database_connection, check_connection):
    database_connection.add_setting(chat_id=1, setting='language', value='es')
    database_connection.add_setting(chat_id=1, setting='language', value='en')

    cursor = check_connection.connection.cursor()
    rows = cursor.execute('SELECT * FROM settings where chat_id=1').fetchall()
    assert len(rows) == 1
    assert rows[0][:3] == (1, 'language', 'en')


def test_get_setting(database_connection):
    database_connection.add_setting(chat_id=1, setting='language', value='es')
    value = database_connection.get_setting(chat_id=1, setting='language')

    assert value == 'es'


def test_get_setting_nonexisting(database_connection):
    value = database_connection.get_setting(chat_id=1, setting='language')

    assert value is None
