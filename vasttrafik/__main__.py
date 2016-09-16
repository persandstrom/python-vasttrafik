# -*- coding: utf-8 -*-
""" Main """

from __future__ import print_function
import argparse
from datetime import datetime

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os
import tabulate
from vasttrafik import JournyPlanner


def get_config_path():
    """Put together the default configuration path based on OS."""
    dir_path = (os.getenv('APPDATA') if os.name == "nt"
                else os.path.expanduser('~'))
    return os.path.join(dir_path, '.vtjp')


def read_config():
    """Read configuration file"""
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(get_config_path())
    if not config.has_section('credentials'):
        config.add_section('credentials')
        config.set('credentials', 'key', '')
        config.set('credentials', 'secret', '')
        write_config(config)
    return config


def write_config(config):
    """Write configuration file"""
    with open(get_config_path(), 'w') as configfile:
        config.write(configfile)


def print_table(document, *columns):
    """ Print json document as table """
    headers = []
    for _, header in columns:
        headers.append(header)
    table = []
    for element in document:
        row = []
        for item, _ in columns:
            if item in element:
                row.append(element[item])
            else:
                row.append(None)
        table.append(row)
    print(tabulate.tabulate(table, headers))


def print_trip_table(document):
    """ Print trip table """
    headers = [
        'Alt.',
        'Name',
        'Time',
        'Track',
        'Direction',
        'Dest.',
        'Track',
        'Arrival']
    table = []
    altnr = 0
    for alternative in document:
        altnr += 1
        first_trip_in_alt = True
        if not isinstance(alternative['Leg'], list):
            alternative['Leg'] = [alternative['Leg']]
        for part in alternative['Leg']:
            orig = part['Origin']
            dest = part['Destination']
            row = [
                altnr if first_trip_in_alt else None,
                part['name'],
                orig['rtTime'] if 'rtTime' in orig else orig['time'],
                orig['track'],
                part['direction'] if 'direction' in part else None,
                dest['name'],
                dest['track'],
                dest['rtTime'] if 'rtTime' in dest else dest['time'],
                ]
            table.append(row)
            first_trip_in_alt = False
    print(tabulate.tabulate(table, headers))


# pylint: disable=too-many-statements, too-many-locals
def main():
    """ Main function """
    config = read_config()
    key = config.get('credentials', 'key')
    secret = config.get('credentials', 'secret')
    parser = argparse.ArgumentParser(
        description=u'Västtrafik journy planner (vtjp)')
    parser.add_argument(
        '-k',
        '--key',
        nargs='?' if key else None,
        default=key,
        help='API key, required argument if credentials not stored')
    parser.add_argument(
        '-s',
        '--secret',
        nargs='?' if secret else None,
        default=secret,
        help='API secret, required argument if credentials not stored')
    service_parser = parser.add_subparsers(
        dest='service',
        help='service to call')

    # STORE CREDENTIALS
    service_parser.add_parser(
        'store',
        help='Store credentials to configuration file')

    # LOCATION
    location_parser = service_parser.add_parser(
        'location',
        help='Get location information, e.g. stops, addresses')
    location_subparser = location_parser.add_subparsers(
        help='method',
        dest='location_method')
    location_name_parser = location_subparser.add_parser(
        'name',
        help='Get stop by name')
    location_name_parser.add_argument(
        'name',
        help='Name of stop')
    location_subparser.add_parser(
        'allstops',
        help='Get all stops')
    location_nearbystops_parser = location_subparser.add_parser(
        'nearbystops',
        help='Get stops nearby location')
    location_nearbystops_parser.add_argument(
        'lat',
        help='latitude')
    location_nearbystops_parser.add_argument(
        'lon',
        help='longitude')
    location_nearbystops_parser = location_subparser.add_parser(
        'nearbyaddress',
        help='Get address nearby location')
    location_nearbystops_parser.add_argument(
        'lat',
        help='latitude')
    location_nearbystops_parser.add_argument(
        'lon',
        help='longitude')

    # ARIVAL BOARD
    arrival_parser = service_parser.add_parser(
        'arrival',
        help='Get arrival board for stop')
    arrival_parser.add_argument(
        'id',
        help='Id or name of stop')
    arrival_parser.add_argument(
        '--date', '-d',
        nargs='?',
        help='The date, default current date')
    arrival_parser.add_argument(
        '--time', '-t',
        nargs='?',
        help='The time, default current time')
    arrival_parser.add_argument(
        '--direction',
        default=None,
        help='Id or name to filter on arrivals from specified direction')

    # DEPARTURE BOARD
    departure_parser = service_parser.add_parser(
        'departure',
        help='Get departure board for stop')
    departure_parser.add_argument(
        'id',
        help='Id or name of stop')
    departure_parser.add_argument(
        '--date', '-d',
        nargs='?',
        help='The date, default current date')
    departure_parser.add_argument(
        '--time', '-t',
        nargs='?',
        help='The time, default current time')
    departure_parser.add_argument(
        '--direction',
        default=None,
        help='Id or name to filter on departures in specified direction')

    # TRIP
    departure_parser = service_parser.add_parser(
        'trip',
        help='Get trip suggestions')
    departure_parser.add_argument(
        'originId',
        help='ID or name of departure stop')
    departure_parser.add_argument(
        'destinationId',
        help='ID or name of destination stop')
    departure_parser.add_argument(
        '--date', '-d',
        nargs='?',
        help='The date, default current date')
    departure_parser.add_argument(
        '--time', '-t',
        nargs='?',
        help='The time, default current time')

    args = parser.parse_args()

    planner = JournyPlanner(
        key=args.key,
        secret=args.secret)

    def name_to_id(attribute):
        """ Check if the stop name has to be convereted to an ID"""
        if not hasattr(args, attribute):
            return
        value = getattr(args, attribute)
        if not value or value.isdigit():
            return
        setattr(args, attribute, planner.location_name(value)[0]['id'])

    # Convert stop names to id if needed
    name_to_id('id')
    name_to_id('originId')
    name_to_id('destinationId')
    name_to_id('direction')

    # PARSE DATE
    date = datetime.now()
    if hasattr(args, 'date') and args.date:
        newdate = datetime.strptime(args.date, '%Y-%m-%d')
        date = date.replace(
            year=newdate.year,
            month=newdate.month,
            day=newdate.day)
    if hasattr(args, 'time') and args.time:
        newtime = datetime.strptime(args.time, '%H:%M')
        date = date.replace(
            hour=newtime.hour,
            minute=newtime.minute)

    # STORE CREDENTIALS
    if args.service == 'store':
        config.set('credentials', 'key', args.key)
        config.set('credentials', 'secret', args.secret)
        write_config(config)

    # LOCATION
    if args.service == 'location':
        if args.location_method == 'allstops':
            print_table(
                planner.location_allstops(),
                ('id', 'ID'),
                ('name', 'Name'),
                ('track', 'Track'))
        if args.location_method == 'name':
            print_table(
                planner.location_name(args.name),
                ('id', 'ID'),
                ('name', 'Name'))
        if args.location_method == 'nearbystops':
            print_table(
                planner.location_nearbystops(args.lat, args.lon),
                ('id', 'ID'),
                ('name', 'Name'),
                ('track', 'Track'))
        if args.location_method == 'nearbyaddress':
            print_table(
                [planner.location_nearbyaddress(args.lat, args.lon)],
                ('name', 'Name'),
                ('lon', 'Longitude'),
                ('lat', 'Latitude'))

    # ARRIVALBOARD
    elif args.service == 'arrival':
        print_table(
            planner.arrivalboard(
                args.id,
                date=date,
                direction=args.direction),
            ('sname', 'Line'),
            ('time', 'Arrival'),
            ('rtTime', 'Prel.Arrival'),
            ('track', 'Track'),
            ('origin', 'Origin'))

    # DEPARTUREBOARD
    elif args.service == 'departure':
        print_table(
            planner.departureboard(
                args.id,
                date=date,
                direction=args.direction),
            ('sname', 'Line'),
            ('time', 'Departure'),
            ('rtTime', 'Prel.Departure'),
            ('track', 'Track'),
            ('direction', 'Direction'))

    # TRIP
    elif args.service == 'trip':
        print_trip_table(
            planner.trip(
                args.originId,
                args.destinationId,
                date=date))

    # IF NOTHING ELSE PRINT HELP
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
