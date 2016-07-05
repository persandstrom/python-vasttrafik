"""
Västtrafik API
"""

import base64
import json
import time as time_module
import requests

TOKEN_URL = 'https://api.vasttrafik.se/token'
API_BASE_URL = 'https://api.vasttrafik.se/bin/rest.exe/v2'


def fetch_token(key, secret):
    """ Get token from key and secret """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(
            (key + ':' + secret).encode()).decode()
        }
    data = {'grant_type': 'client_credentials'}

    response = requests.post(TOKEN_URL, data=data, headers=headers)
    obj = json.loads(response.content.decode('UTF-8'))
    return obj['access_token']


def get_node(response, *ancestors):
    """ Traverse tree to node """
    document = response
    for ancestor in ancestors:
        if ancestor not in document:
            return {}
        else:
            document = document[ancestor]
    return document


class JournyPlanner:
    """ Journy planner class"""

    def __init__(self, key, secret, response_format=''):
        self.token = fetch_token(key, secret)
        self.format = 'json' if response_format == 'JSON' else ''

    # LOCATION

    def location_allstops(self):
        """ location.allstops """
        response = self.request(
            'location.allstops')
        return get_node(response, 'LocationList', 'StopLocation')

    def location_nearbystops(self, origin_coord_lat, origin_coord_long):
        """ location.nearbystops """
        response = self.request(
            'location.nearbystops',
            originCoordLat=origin_coord_lat,
            originCoordLong=origin_coord_long)
        return get_node(response, 'LocationList', 'StopLocation')

    def location_nearbyaddress(self, origin_coord_lat, origin_coord_long):
        """ location.nearbyaddress """
        response = self.request(
            'location.nearbyaddress',
            originCoordLat=origin_coord_lat,
            originCoordLong=origin_coord_long)
        return get_node(response, 'LocationList', 'CoordLocation')

    def location_name(self, name):
        """ location.name """
        response = self.request(
            'location.name',
            input=name)
        return get_node(response, 'LocationList', 'StopLocation')

    # ARRIVAL BOARD

    def arrivalboard(self, stop_id, date=None, time=None):
        """ arrivalBoard """
        date = date if date else time_module.strftime("%Y-%m-%d")
        time = time if time else time_module.strftime("%H:%M")
        response = self.request(
            'arrivalBoard',
            id=stop_id,
            date=date,
            time=time)
        return get_node(response, 'ArrivalBoard', 'Arrival')

    # DEPARTURE BOARD

    def departureboard(self, stop_id, date=None, time=None):
        """ departureBoard """
        date = date if date else time_module.strftime("%Y-%m-%d")
        time = time if time else time_module.strftime("%H:%M")
        response = self.request(
            'departureBoard',
            id=stop_id,
            date=date,
            time=time)
        return get_node(response, 'DepartureBoard', 'Departure')

    # TRIP

    def trip(self, origin_id, dest_id, date=None, time=None):
        """ trip """
        date = date if date else time_module.strftime("%Y-%m-%d")
        time = time if time else time_module.strftime("%H:%M")
        response = self.request(
            'trip',
            originId=origin_id,
            destId=dest_id,
            date=date,
            time=time)
        return get_node(response, 'TripList', 'Trip')

    def request(self, service, **parameters):
        """ request builder """
        urlformat = "{baseurl}/{service}?{parameters}&format={response_format}"
        url = urlformat.format(
            baseurl=API_BASE_URL,
            service=service,
            parameters="&".join([
                "{}={}".format(key, value) for key, value in parameters.items()
                ]),
            response_format=self.format)

        headers = {'Authorization': 'Bearer ' + self.token}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return json.loads(res.content.decode('UTF-8'), 'UTF-8')
        else:
            raise Exception('Error: ' + str(res.status_code) +
                            str(res.content))
