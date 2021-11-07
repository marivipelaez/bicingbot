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

from bicingbot.database_conn import DatabaseConnection


class DatabaseMigration(object):
    """
    Updates a database schema
    """

    def __init__(self, database='bicingbot.db', config_path=None):
        self.connection = DatabaseConnection(database, config_path).connection

    def create_schema(self):
        """
        Creates a complete schema of the database
        """
        self.create_initial_schema()
        self.update_schema_table_settings()
        self.connection.close()

    def create_initial_schema(self):
        """
        Creates the first schema of the database
        """
        cursor = self.connection.cursor()

        # Create groups table
        cursor.execute('''CREATE TABLE groups (chat_id INTEGER NOT NULL,
                                               name TEXT NOT NULL,
                                               station_id INTEGER NOT NULL,
                                               created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                                               PRIMARY KEY (chat_id, name, station_id))''')
        self.connection.commit()

    def update_schema_table_settings(self):
        """
        Update the schema of the database adding settings table.
        """
        cursor = self.connection.cursor()

        # Create groups table
        cursor.execute('''CREATE TABLE settings (chat_id INTEGER NOT NULL,
                                                 setting TEXT NOT NULL,
                                                 value INTEGER NOT NULL,
                                                 created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                                                 PRIMARY KEY (chat_id, setting))''')
        self.connection.commit()
