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

import os
import sqlite3


class DatabaseConnection(object):
    """
    Creates a new database connection
    """
    connection = None

    def __init__(self, database='bicingbot.db'):
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'conf')
        self.connection = sqlite3.connect(os.path.join(config_path, database))

    def close(self):
        """
        Closes current connection
        """
        self.connection.close()

    def create_schema(self):
        """
        Creates the schema of the database
        """
        cursor = self.connection.cursor()

        # Create groups table
        cursor.execute('''CREATE TABLE groups (chat_id INTEGER NOT NULL,
                                               name TEXT NOT NULL,
                                               station_id INTEGER NOT NULL,
                                               created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                                               PRIMARY KEY (chat_id, name, station_id))''')
        self.connection.commit()

    def create_group(self, chat_id, name, stations):
        """
        Inserts a new group definition

        :param chat_id: user identifier
        :param name: name of the group
        :param stations: list of integers of stations ids
        """
        cursor = self.connection.cursor()
        for station_id in stations:
            cursor.execute("INSERT INTO groups (chat_id, name, station_id) VALUES (?,?,?)", (chat_id, name, station_id))
        self.connection.commit()

    def get_group(self, chat_id, name):
        """
        Retrieves all the information of a group

        :param chat_id: user that created the group
        :param name: group to read
        :return: a dictionary with the information of the group or None if it does not exist
        """
        cursor = self.connection.cursor()
        stations = []
        for row in cursor.execute('SELECT station_id FROM groups WHERE chat_id=? AND name=?', (chat_id, name)):
            stations.append(row[0])
        if stations:
            return {'chat_id': chat_id, 'name': name, 'stations': stations}
        return None

    def get_groups_names(self, chat_id):
        """
        Retrieves all groups from a chat_id

        :param chat_id: user that created the groups
        :return: a list of group names
        """
        cursor = self.connection.cursor()
        groups_names = []
        for row in cursor.execute('SELECT name FROM groups WHERE chat_id=? group by name', (chat_id,)):
            groups_names.append(row[0])
        return groups_names

    def delete_group(self, chat_id, name):
        """
        Deletes an existing group

        :param chat_id: user identifier
        :param name: name of the group
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM groups WHERE chat_id=? AND name=?", (chat_id, name))
        self.connection.commit()
