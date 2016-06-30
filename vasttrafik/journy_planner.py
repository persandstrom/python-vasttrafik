"""
Västtrafik API
"""

import base64
import json
import time as time_module
import requests

TOKEN_URL = 'https://api.vasttrafik.se/token'
API_BASE_URL = 'https://api.vasttrafik.se/bin/rest.exe/v2'
CONSUMER_KEY = '<insert your CONSUMER_KEY here>'
CONSUMER_SECRET = '<insert your CONSUMER_SECRET here>'


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


class JournyPlanner:
    """ Journy planner class"""

    def __init__(self, response_format='', key=CONSUMER_KEY,
                 secret=CONSUMER_SECRET):
        self.token = fetch_token(key, secret)
        self.format = '&format=json' if response_format == 'JSON' else ''

    # LOCATION

    def get_all_stops(self):
        """ /location.allstops """
        data = self.get('/location.allstops')
        return data['LocationList']['StopLocation']

    def get_nearby_stops(self, lat, lon):
        """ /location.nearbystops """
        data = self.get(
            '/location.nearbystops?originCoordLat=' + str(lat) +
            '&originCoordLong=' + str(lon))
        return data['LocationList']['StopLocation']

    def get_nearby_address(self, lat, lon):
        """ /location.nearbyaddress """
        data = self.get(
            '/location.nearbyaddress?originCoordLat=' + str(lat) +
            '&originCoordLong=' + str(lon))
        return data['LocationList']['CoordLocation']

    def get_stops_by_name(self, query):
        """ /location.name """
        data = self.get('/location.name?input=' + query)
        return data['LocationList']['StopLocation']

    # TRIP

    def get_arrivalboard(self, stop_id, date=None, time=None):
        """ /arrivalBoard endpoint """
        if date and time:
            data = self.get('/arrivalBoard?id=' + str(stop_id) + '&date=' +
                            date + '&time=' + time)
        else:
            data = self.get('/arrivalBoard?id=' + str(stop_id) + '&date=' +
                            time_module.strftime("%Y-%m-%d") +
                            '&time=' + time_module.strftime("%H:%M"))
        return data['ArrivalBoard']['Arrival']

    def get_departureboard(self, stop_id, date=None, time=None):
        """ /departureBoard endpoint """
        if date and time:
            data = self.get('/departureBoard?id=' + str(stop_id) +
                            '&date=' + date +
                            '&time=' + time)
        else:
            data = self.get('/departureBoard?id=' + str(stop_id) +
                            '&date=' + time_module.strftime("%Y-%m-%d") +
                            '&time=' + time_module.strftime("%H:%M"))
            return data['DepartureBoard']['Departure']

    def get(self, endpoint):
        """ request builder """
        url = API_BASE_URL + endpoint + self.format

        headers = {'Authorization': 'Bearer ' + self.token}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return json.loads(res.content.decode('UTF-8'), 'UTF-8')
        else:
            raise Exception('Error: ' + str(res.status_code) +
                            str(res.content))
