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

from bicingbot.database_conn import DatabaseConnection
import os


def test_create_group():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'conf')
    os.remove(os.path.join(config_path, 'bicingbot_test.db'))
    database_connection = DatabaseConnection(database='bicingbot_test.db')
    database_connection.create_schema()
    database_connection.create_group(chat_id=1, name='test_group', stations=[1, 2, 3])

    cursor = database_connection.connection.cursor()
    rows = cursor.execute('select * from groups').fetchall()
    database_connection.close()
    assert len(rows) == 3
    assert rows[0][:3] == (1, 'test_group', 1)
    assert rows[1][:3] == (1, 'test_group', 2)
    assert rows[2][:3] == (1, 'test_group', 3)
    assert rows[0][3] is not None
    assert rows[0][3] == rows[1][3]
    assert rows[0][3] == rows[2][3]
