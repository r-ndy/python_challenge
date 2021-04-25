import argparse
import os
from pathlib import Path
import pprint

import lookup
from populate import populate
from query import query


def test_populate_default_test_file():
    populate.populate()


def test_populate_from_file():
    current_path = Path(__file__).resolve().parent
    file_name = os.path.join(current_path, 'populate',
                             'test_data', 'list_of_ips.txt')
    populate.populate(file_name)


def test_populate_force_update_cache():
    populate.populate(force_update_cache=True)


def test_get_geo_ip_info():
    pp = _get_default_pretty_printer()
    pp.pprint(lookup.get_geo_ip_info('244.36.171.60'))
    print('\n')


def test_get_rdap_info():
    pp = _get_default_pretty_printer()
    pp.pprint(lookup.get_rdap_info('244.36.171.60'))
    print('\n')


def test_get_geo_ip_info_force_update_cache():
    pp = _get_default_pretty_printer()
    pp.pprint(lookup.get_geo_ip_info('244.36.171.60', force_update_cache=True))
    print('\n')


def test_get_rdap_info_force_update_cache():
    pp = _get_default_pretty_printer()
    pp.pprint(lookup.get_rdap_info('244.36.171.60', force_update_cache=True))
    print('\n')


def test_single_geo_ip_query():
    pp = _get_default_pretty_printer()

    query_dict = {'ip': {'op': '=', 'value': '1.34.194.31'}}

    print('Query:')
    pp.pprint(query_dict)

    print('\n\n', 'Result:')
    results = query.query_geo_ip(query_dict)
    pp.pprint(results)
    print('\n\n', 'Number of results:', len(results))
    print('\n')


def test_nested_geo_ip_query():
    pp = _get_default_pretty_printer()

    query_dict = {
        'and': [
            {'country_name': {'op': '=', 'value': 'United States'}},
            {'region_name': {'op': 'in', 'value': ['Michigan', 'Tennessee']}},
            {
                'or': [
                    {'metro_code': {'op': '=', 'value': 0}},
                    {'metro_code': {'op': '>', 'value': 100}},
                ]
            },
        ]
    }

    print('Query:')
    pp.pprint(query_dict)

    print('\n\n', 'Result:')
    results = query.query_geo_ip(query_dict)
    pp.pprint(results)
    print('\n\n', 'Number of results:', len(results))
    print('\n')


def test_single_rdap_query():
    pp = _get_default_pretty_printer()

    query_dict = {
        "country": {
            'op': '=',
            'value': 'JP'
        }
    }

    print('Query:')
    pp.pprint(query_dict)

    print('\n\n', 'Result:')
    results = query.query_rdap(query_dict)
    pp.pprint(results)
    print('\n\n', 'Number of results:', len(results))
    print('\n')


def test_nested_rdap_query():
    pp = _get_default_pretty_printer()

    query_dict = {
        'and': [
            {'country': {'op': '=', 'value': 'JP'}},
            {'ipVersion': {'op': '=', 'value': 'v4'}},
            {
                'or': [
                    {'objectClassName': {'op': '=', 'value': 'ip network'}},
                    {'port43': {'op': '!=', 'value': 'whois.apnic.net'}},
                ]
            },
        ]
    }

    print('Query:')
    pp.pprint(query_dict)

    print('\n\n', 'Result:')
    results = query.query_rdap(query_dict)
    pp.pprint(results)
    print('\n\n', 'Number of results:', len(results))
    print('\n')


def _get_default_pretty_printer():
    return pprint.PrettyPrinter(indent=4)


def main():
    examples_names = [
        'test_populate_default_test_file',
        'test_populate_from_file',
        'test_populate_force_update_cache',
        'test_get_geo_ip_info',
        'test_get_rdap_info',
        'test_get_geo_ip_info_force_update_cache',
        'test_get_rdap_info_force_update_cache',
        'test_single_geo_ip_query',
        'test_nested_geo_ip_query',
        'test_single_rdap_query',
        'test_nested_rdap_query',
    ]

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--list-examples', action='store_true', dest='list_examples',
        help='It shows the list of functions available to run as test examples.')
    argument_parser.add_argument('--run', action='store', dest='run_function',
                                 help='Runs an example')

    args = argument_parser.parse_args()

    if args.list_examples:
        for example in examples_names:
            print(example)
    elif args.run_function:
        if args.run_function in examples_names:
            eval(f'{args.run_function}()')
        else:
            print(f'{args.run_function} doesn\'t exist')


if __name__ == "__main__":
    main()
