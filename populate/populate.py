import os
from pathlib import Path

from parser import parser
import lookup


def populate(file_name=None, force_update_cache=False):
    """
    Populates GEO IP and RDAP from the IP addresses found
    by the file provided or by the default file.
    """

    if file_name:
        if not os.path.isfile(file_name):
            print('File not found: ', file_name)
            return
    else:
        # uses default test file
        current_path = Path(__file__).resolve().parent
        file_name = os.path.join(current_path, 'test_data', 'list_of_ips.txt')

    print('Populating IP Addresses from', file_name)

    raw_text = parser.get_text_from_file(file_name)
    ips_list = parser.parse_ips(raw_text)

    if ips_list:
        len_ips_len = len(ips_list)
        print('IP addresses found: ', len(ips_list))
        for index, ip_address in enumerate(ips_list):
            print(f'IP number {index + 1} from {len_ips_len} ({ (index + 1) * 100 // len_ips_len }%)')
            lookup.get_geo_ip_info(ip_address, force_update_cache=force_update_cache)
            lookup.get_rdap_info(ip_address, force_update_cache=force_update_cache)
    else:
        print('No IP addresses where found')