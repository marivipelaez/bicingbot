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

import mock
import pytest
import requests_mock
from requests import ConnectionError

from bicingbot.bicing import Bicing, GET_STATION_URL, StationNotFoundError

logger = logging.getLogger(__name__)

# Bicing mock responses
generic_response = '{"parametros_filtro": {"station": ["text", "%s", "station"]}, ' \
                   '"estacions_icon": "/modules/custom/mapa_disponibilitat/assets/icons/estacions.png", ' \
                   '"stations": %s, ' \
                   '"url_icon4": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio4.png", ' \
                   '"url_icon5": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio5.png", ' \
                   '"url_icon2": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio2.png", ' \
                   '"url_icon3": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio3.png", ' \
                   '"url_icon": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio.png"}'
mock_found_station = '[{"status": 1, "transition_end": "", "disponibilidad": 50, "longitude": ' \
                     '2.201656, "transition_start": "", "electrical_bikes": 0, "type_bicing": 2, "bikes": 15, ' \
                     '"mechanical_bikes": 15, "streetNumber": "", "latitude": 41.402454, "slots": 17, "type": ' \
                     '"BIKE", "id": "154", "streetName": "154 - C/ PUJADES, 191", ' \
                     '"icon": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio4-50.png"}]'
mock_error_station = '{"error":"unknown error"}'


@requests_mock.Mocker()
def test_get_station(req_mock):
    station_id = 172
    expected_station = {u'status': 1, u'transition_end': u'', u'disponibilidad': 50, u'longitude': 2.201656,
                        u'transition_start': u'', u'electrical_bikes': 0, u'type_bicing': 2, u'bikes': 15,
                        u'mechanical_bikes': 15, u'streetNumber': u'', u'latitude': 41.402454, u'slots': 17,
                        u'type': u'BIKE', u'id': u'154', u'streetName': u'154 - C/ PUJADES, 191',
                        u'icon': u'/modules/custom/mapa_disponibilitat/assets/icons/ubicacio4-50.png'}
    mock_found_response = generic_response % (station_id, mock_found_station)
    req_mock.post(GET_STATION_URL.format(station_id), content=mock_found_response)

    station = Bicing().get_station(station_id)
    assert station == expected_station


@requests_mock.Mocker()
def test_get_station_not_found(req_mock):
    station_id = 9999
    mock_not_found_response = generic_response % (station_id, [])
    req_mock.post(GET_STATION_URL.format(station_id), content=mock_not_found_response)

    with pytest.raises(StationNotFoundError) as excinfo:
        Bicing().get_station(station_id)
    assert str(excinfo.value) == 'Station {} not found'.format(station_id)


@mock.patch('bicingbot.bicing.requests.post')
def test_get_station_url_error(req_post_mock):
    station_id = 154
    req_post_mock.side_effect = ConnectionError('exception error')

    with pytest.raises(Exception) as excinfo:
        Bicing().get_station(station_id)
    assert str(excinfo.value) == "Error requesting station {}: exception error".format(station_id)


@requests_mock.Mocker()
def test_get_station_error(req_mock):
    station_id = 8888
    req_mock.post(GET_STATION_URL.format(station_id), content=mock_error_station)

    with pytest.raises(Exception) as excinfo:
        Bicing().get_station(station_id)
    assert str(excinfo.value) == "Error requesting station {}: 'stations'".format(station_id)
