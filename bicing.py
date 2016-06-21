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

import requests

GET_STATIONS_URL = 'http://wservice.viabicing.cat/v2/stations'
GET_STATION_URL = GET_STATIONS_URL + '/{}'

logger = logging.getLogger(__name__)


class StationNotFoundError(Exception):
    pass


class Bicing(object):
    """

    """

    def get_station(self, station_id):
        """
        Retrieves station status from Bicing API
        :param station_id: id of the station
        :return: a dict with the status of the given station
        """
        try:
            reponse_json = requests.get(GET_STATION_URL.format(station_id)).json()
        except Exception as ex:
            logger.warning('Error requesting station {}: {}'.format(station_id, ex))
            raise ex

        try:
            station = reponse_json['stations'][0]
        except KeyError:
            error = reponse_json['error']
            if error == 'not found':
                error_message = 'Station {} not found'.format(station_id)
                logger.warning(error_message)
                raise StationNotFoundError(error_message)
            else:
                error_message = 'Station {} can not be read due to {}'.format(station_id, error)
                logger.warning(error_message)
                raise Exception(error_message)
        logger.debug('status[{}] = {}'.format(station_id, station))

        return station
