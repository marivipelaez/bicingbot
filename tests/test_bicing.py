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
import logging
import unittest

import mock
import requests_mock
from nose.tools import assert_equal, assert_raises
from requests import ConnectionError

from app.bicing import Bicing, GET_STATION_URL, StationNotFoundError

logger = logging.getLogger(__name__)

# Bicing mock responses
mock_found_station = '{"stations":[{"id":"154","type":"BIKE","latitude":"41.402454","longitude":"2.201656",' \
                     '"streetName":"Pujades","streetNumber":"191","altitude":"10","slots":"15","bikes":"11",' \
                     '"nearbyStations":"141, 153, 165, 382","status":"OPN"}],"updateTime":1466443268}'
mock_not_found_station = '{"error":"not found"}'
mock_error_station = '{"error":"unknown error"}'


class TestBicing(unittest.TestCase):
    """

    """

    @requests_mock.Mocker()
    def test_get_station(self, req_mock):
        station_id = 154
        expected_station = {'id': '154', 'type': 'BIKE', 'latitude': '41.402454', 'longitude': '2.201656',
                            'streetName': 'Pujades', 'streetNumber': '191', 'altitude': '10', 'slots': '15',
                            'bikes': '11', 'nearbyStations': '141, 153, 165, 382', 'status': 'OPN'}
        req_mock.get(GET_STATION_URL.format(station_id), content=mock_found_station)

        station = Bicing().get_station(station_id)
        assert_equal(station, expected_station)

    @requests_mock.Mocker()
    def test_get_station_not_found(self, req_mock):
        station_id = 9999
        req_mock.get(GET_STATION_URL.format(station_id), content=mock_not_found_station)

        assert_raises(StationNotFoundError, Bicing().get_station, station_id)

    @mock.patch('app.bicing.requests.get')
    def test_get_station_url_error(self, req_get_mock):
        station_id = 154
        req_get_mock.side_effect = ConnectionError('exception error')

        with assert_raises(Exception) as context:
            Bicing().get_station(station_id)

        assert_equal(context.exception.message, 'exception error')

    @requests_mock.Mocker()
    def test_get_station_error(self, req_mock):
        station_id = 8888
        req_mock.get(GET_STATION_URL.format(station_id), content=mock_error_station)

        with assert_raises(Exception) as context:
            Bicing().get_station(station_id)

        assert_equal(context.exception.message, 'Station {} can not be read due to unknown error'.format(station_id))
