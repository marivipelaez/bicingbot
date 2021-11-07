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

import logging

import requests

GET_STATION_URL = 'https://www.bicing.barcelona/get-stations'
POST_BODY = 'station%5B%5D=text&station%5B%5D={station_id}&station%5B%5D=station'

logger = logging.getLogger(__name__)


class StationNotFoundError(Exception):
    pass


class Bicing(object):
    """

    """

    @staticmethod
    def get_station(station_id):
        """
        Retrieves station status from Bicing API

        :param station_id: id of the station
        :return: a dict with the status of the given station
        """
        try:
            response = requests.post(GET_STATION_URL, data=POST_BODY.format(station_id=station_id),
                                     headers={'Content-type': 'application/x-www-urlencoded'})
            stations = response.json()['stations']
        except Exception as ex:
            error_message = 'Error requesting station {}: {}'.format(station_id, ex)
            logger.warning(error_message)
            raise Exception(error_message)

        if len(stations) == 0:
            error_message = 'Station {} not found'.format(station_id)
            logger.warning(error_message)
            raise StationNotFoundError(error_message)

        station = stations[0]
        logger.debug('status[{}] = {}'.format(station_id, station))

        return station
