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


class Client:
    """ Journy planner class"""

    def __init__(self, response_format='', key=CONSUMER_KEY,
                 secret=CONSUMER_SECRET):
        self.token = fetch_token(key, secret)
        self.format = '&format=json' if response_format == 'JSON' else ''

    # def get_journey_detail(self, ref, query_params=None):
    #     """ /journeyDetail endpoint """
    #     return ''

    # /location endpoint
    # /location.allstops
    # def get_all_stops(self, query_params=None):
    #     raise Exception("Error: Can't get this endpoint to work."
    #                     " No idea why. Should be implemented in future.")

    def get_nearby_stops(self, lat, long):
        """ /location.nearbystops """
        data = self.get(
            '/location.nearbystops?originCoordLat=' + str(lat) +
            '&originCoordLong=' + str(long))
        return data['LocationList']['StopLocation']

    def get_stops_by_name(self, query, query_params=None):
        """ /location.name """
        data = self.get('/location.name?input=' + query, query_params)
        return data['LocationList']['StopLocation']

    # /location.nearbyaddress
    # def get_nearby_address(self, lat, long, query_params=None):
    #     data = self.get('/location.name?input=' + query, query_params)
    #     return data['LocationList']['CoordLocation']

    def get_arrivals(self, stop_id, date=None, time=None, query_params=None):
        """ /arrivalBoard endpoint """
        if date is not None and time is not None:
            data = self.get('/arrivalBoard?id=' + str(stop_id) + '&date=' +
                            date + '&time=' + time, query_params)
        else:
            data = self.get('/arrivalBoard?id=' + str(stop_id) + '&date=' +
                            time_module.strftime("%Y-%m-%d") +
                            '&time=' + time_module.strftime("%H:%M"),
                            query_params)
        return data['ArrivalBoard']['Arrival']

    def get_departures(self, stop_id, date=None, time=None, query_params=None):
        """ /departureBoard endpoint """
        if date is not None and time is not None:
            data = self.get('/departureBoard?id=' + str(stop_id) +
                            '&date=' + date +
                            '&time=' + time, query_params)
        else:
            data = self.get('/departureBoard?id=' + str(stop_id) +
                            '&date=' + time_module.strftime("%Y-%m-%d") +
                            '&time=' + time_module.strftime("%H:%M"),
                            query_params)
            return data['DepartureBoard']['Departure']

    # def calculate_trip(self, query_params=None):
    #     """ trip endpoint """
    #     return ''

    def get(self, endpoint, query_params=None):
        """ request builder """
        url = API_BASE_URL + endpoint + self.format
        if query_params is not None:
            for key in query_params:
                url += '&' + key + '=' + query_params[key]

        headers = {'Authorization': 'Bearer ' + self.token}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return json.loads(res.content.decode('UTF-8'), 'UTF-8')
        else:
            raise Exception('Error: ' + str(res.status_code) +
                            str(res.content))
