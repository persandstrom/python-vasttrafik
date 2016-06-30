#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Testmodule """

from __future__ import print_function
import argparse
import pprint
import tabulate
from vasttrafik import JournyPlanner


def print_table(document, *columns):
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

# pylint: disable=C0103
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Västtrafik journy planner')
    parser.add_argument(
        'key')
    parser.add_argument(
        'secret')
    service_parser = parser.add_subparsers(
        dest='service',
        help='service')

    # LOCATION
    location_parser = service_parser.add_parser(
        'location')
    location_subparser = location_parser.add_subparsers(
        help='method',
        dest='location_method')
    location_name_parser = location_subparser.add_parser(
        'name')
    location_name_parser.add_argument(
        'name')
    location_allstops_parser = location_subparser.add_parser(
        'allstops')
    location_nearbystops_parser = location_subparser.add_parser(
        'nearbystops')
    location_nearbystops_parser.add_argument(
        'lat')
    location_nearbystops_parser.add_argument(
        'lon')
    location_nearbystops_parser = location_subparser.add_parser(
        'nearbyaddress')
    location_nearbystops_parser.add_argument(
        'lat')
    location_nearbystops_parser.add_argument(
        'lon')

    # ARIVAL BOARD
    arrival_parser = service_parser.add_parser(
        'arrivalboard')
    arrival_parser.add_argument(
        'id')
    arrival_parser.add_argument(
        'date',
        nargs='?')
    arrival_parser.add_argument(
        'time',
        nargs='?')
    
    # DEPARTURE BOARD
    departure_parser = service_parser.add_parser(
        'departureboard')
    departure_parser.add_argument(
        'id')
    departure_parser.add_argument(
        'date',
        nargs='?')
    departure_parser.add_argument(
        'time',
        nargs='?')


    args = parser.parse_args()

    planner = JournyPlanner(
        response_format='JSON',
        key=args.key,
        secret=args.secret)

    if hasattr(args, 'id') and not args.id.isdigit():
        args.id = planner.get_stops_by_name(args.id)[0]['id']

    # LOCATION
    if args.service == 'location':
        if args.location_method == 'allstops':
            pprint.pprint(planner.get_all_stops())
        if args.location_method == 'name':
            print_table(
                planner.get_stops_by_name(args.name),
                ('id', 'ID'),
                ('name', 'Name'))
        if args.location_method == 'nearbystops':
            print_table(
                planner.get_nearby_stops(args.lat, args.lon),
                ('id', 'ID'),
                ('name', 'Name'),
                ('track', 'Track'))
        if args.location_method == 'nearbyaddress':
            print_table(
                [planner.get_nearby_address(args.lat, args.lon)],
                ('name', 'Name'),
                ('lon', 'Longitude'),
                ('lat', 'Latitude'))

    # ARRIVALBOARD
    if args.service == 'arrivalboard':
        print_table(
            planner.get_arrivalboard(args.id, args.date, args.time),
            ('sname', 'Line'),
            ('time', 'Arrival'),
            ('rtTime', 'Prel.Arrival'),
            ('track', 'Track'))


    # DEPARTUREBOARD
    if args.service == 'departureboard':
        print_table(
            planner.get_departureboard(args.id, args.date, args.time),
            ('sname', 'Line'),
            ('time', 'Departure'),
            ('rtTime', 'Prel.Departure'),
            ('track', 'Track'))
