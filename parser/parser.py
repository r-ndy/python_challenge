import re

def get_text_from_file(file_name: str) -> str:
    """
    Returns the content from a file text.
    """
    try:
        the_file = open(file_name, 'r')
        text_from_file = the_file.read()
        return text_from_file
    except Exception as ex:
        print('Problem opening the file', file_name)
        print(ex)


def parse_ips(raw_text: str) -> list:
    """
    Returns a list of all ip addresses. 
    """
    found_ips_list = re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', raw_text)
    return found_ips_list
