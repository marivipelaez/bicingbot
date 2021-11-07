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


class CallbackQuery(object):
    def __init__(self, id, data=None, message_id=None):
        self.id = id
        self.data = data
        self.message = Message(message_id)


class Message(object):
    def __init__(self, message_id):
        self.message_id = message_id
