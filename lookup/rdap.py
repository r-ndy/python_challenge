import json
import requests
import os
from pathlib import Path


def get_rdap_info(ip_address, force_update_cache=False):
    """
    Gets rdap information about from ip address
    https://rdap.arin.net
    """
    print('Retrieving RDAP from', ip_address)

    rdap_info = None
    if not force_update_cache:
        rdap_info = get_rdap_info_from_cache(ip_address)

    if not rdap_info:
        api_url = f'https://rdap.arin.net/registry/ip/{ip_address}'
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        response = requests.get(api_url, headers=headers)

        if response.status_code >= 429 and response.status_code < 500:
            alt_api_url = f'https://www.rdap.net/ip/{ip_address}'
            alt_response = requests.get(alt_api_url, headers=headers)
            rdap_info = json.loads(alt_response.content.decode('utf-8'))
            store_rdap_info_in_cache(ip_address, rdap_info)
            return rdap_info
        elif response.status_code == 200:
            rdap_info = json.loads(response.content.decode('utf-8'))
            store_rdap_info_in_cache(ip_address, rdap_info)
            return rdap_info
        else:
            print('Something went wrong obtaing RDAP from', ip_address)

    return rdap_info


def store_rdap_info_in_cache(ip_address: str, rdap_info: dict):
    """
    Creates a JSON file with the info found
    """
    file_name = rdap_info_cache_file_name(ip_address)
    with open(file_name, 'w') as json_file:
        json_file.write(json.dumps(rdap_info, indent=4))


def get_rdap_info_from_cache(ip_address: str) -> dict:
    """
    Creates a JSON file with the info found
    """
    file_name = rdap_info_cache_file_name(ip_address)
    if os.path.isfile(file_name):
        with open(file_name, 'r') as json_file:
            return json.load(json_file)

    return None

def rdap_info_cache_directory() -> str:
    """
    Gets the location of the cache directory
    """
    current_path = Path(__file__).resolve().parent
    return os.path.join(current_path, 'cache', 'rdap')


def rdap_info_cache_file_name(ip_address: str) -> str:
    """
    Gets file location in the cache
    """
    return os.path.join(rdap_info_cache_directory(), f'{ip_address}.json')
