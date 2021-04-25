import json
import requests
import os
from pathlib import Path


def get_geo_ip_info(ip_address: str, force_update_cache=False) -> dict:
    """
    Gets geolocation information from an ip address
    using https://freegeoip.app

    Example
    {'ip': '208.128.240.230', 'country_code': 'US', 
    'country_name': 'United States', 'region_code': '', 
    'region_name': '', 'city': '', 'zip_code': '',
    'time_zone': 'America/Chicago', 'latitude': 37.751, 
    'longitude': -97.822, 'metro_code': 0}
    """
    print('Retrieving GEO IP from', ip_address)

    geo_ip_info = None
    if not force_update_cache:
        geo_ip_info = get_geo_ip_info_from_cache(ip_address)

    if not geo_ip_info:
        api_url = f'https://freegeoip.app/json/{ip_address}'
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            geo_ip_info = json.loads(response.content.decode('utf-8'))
            store_geo_ip_info_in_cache(ip_address, geo_ip_info)
            return geo_ip_info
        else:
            print('Something went wrong obtaing GEO IP from', ip_address)

    return geo_ip_info


def store_geo_ip_info_in_cache(ip_address: str, geo_ip_info: dict):
    """
    Creates a JSON file with the info found
    """
    file_name = geo_ip_info_cache_file_name(ip_address)
    with open(file_name, 'w') as json_file:
        json_file.write(json.dumps(geo_ip_info, indent=4))


def get_geo_ip_info_from_cache(ip_address: str) -> dict:
    """
    Creates a JSON file with the info found
    """
    file_name = geo_ip_info_cache_file_name(ip_address)
    if os.path.isfile(file_name):
        with open(file_name, 'r') as json_file:
            return json.load(json_file)

    return None

def geo_ip_info_cache_directory() -> str:
    """
    Gets the location of the cache directory.
    """
    current_path = Path(__file__).resolve().parent
    return os.path.join(current_path, 'cache', 'geo_ip')

def geo_ip_info_cache_file_name(ip_address: str) -> str:
    """
    Gets file location in the cache
    """
    return os.path.join(geo_ip_info_cache_directory(), f'{ip_address}.json')
