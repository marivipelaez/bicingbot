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

import re

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


def normalize_command_name(text):
    """
    Prepares the input text to be treated as a command: to lower, remove / chars
    :param text: input text
    :return: normalized text
    """
    return (text[1:] if text.startswith('/') else text).lower()


def pad_number(num):
    """
    If given number has only one digit, a new string with two spaces in the left is returned. Otherwise, the same
     string is returned.

    :param num: string with an integer
    :return: padded string
    """
    if int(num) < 10:
        return '  ' + num
    return num


def compact_address(address):
    """
    Reduces address length to fit in the message

    :param address: street name
    :return: compacted street name
    """
    max_length = 14
    stop_words = ['Carrer ', 'de ', 'del ']
    for word in stop_words:
        address = address.replace(word, '')
    return address[:max_length]


def is_integer(text):
    """
    Checks if the given text is an integer

    :param text: string to validate
    :return: True if the text is an integer, False otherwise
    """
    return re.match("^[\d]+$", text)


def grouper(iterable):
    """
    Return a list of elements in tuples of 3 elements
    s -> (s0, s1, s2), (s3, s4, s5), ..."

    :param iterable: list to be ordered
    :return: the list of elements in tuples of 3 elements
    """
    args = [iter(iterable)] * 3
    return zip_longest(*args)
