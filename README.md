# Geo IP and RDAP Lookup
# Main goal
Create a program that will read a given set of IPs, perform Geo IP and RDAP lookups, and accept a query to filter results.
# Structure
```bash
├── LICENSE
├── README.md
├── __init__.py
├── examples.py
├── lookup
│   ├── cache
│   │   ├── geo_ip
│   │   └── rdap
│   ├── __init__.py
│   ├── geo_ip.py
│   └── rdap.py
├── parser
│   ├── __init__.py
│   └── parser.py
├── populate
│   ├── test_data
│   │   └── list_of_ips.txt
│   ├── __init__.py
│   ├── populate.py
└──  query
│   ├── __init__.py
│   └── query.py
```

# Features
This program will read a text file and will parse the IP addresses, perform Geo IP and RDAP lookups, and create queries to filter results. Each component is decoupled from the others and easy to use. This challenge was tested using python 3.6.9. There are four components in this package:
- Lookup
    - Geo IP
    - RDAP
- Parser
- Populate
- Query
    - Geo IP
    - RDAP
<br>
   
## Lookup
This package has modules to perform Geo IP and RDAP lookups.
### Geo IP Lookup
This modulue contains a main function to perform a geo IP lookup. The function takes an IP address as input, will perform a GET request to freegeoip.app and parse the output as a dictionary, this result is storaged in JSON file as cache.<br>
It also contains other helpful functions.
### RDAP Lookup
This module contains a main function to perform a RDAP lookup. The function takes an IP address as input, will perform a GET request to rdap.net and parse the output as a dictionary, this result is storaged in JSON file as cache.<br>
It also contains other helpful functions.
## Parser
This module contains functions to take a text file as input and extract the IP addresses from it, then returns a list of these IP addresses.
## Populate
This module allows to load in cache the GEO IP and RDAP from the IPs found from a specific text file or from a test file provided by the module.
## Query
This module contains functions to create queries using filters in order to find specific information from the GEO IP and RDAP cache. It uses query a language specified by using dictionaries.

# Installation 
```bash
# Clone this repository
$ https://github.com/r-ndy/python_challenge.git

# Go into the repository to test it
$ cd python_challenge

# Or move the files into your project
$ mv python_challenge my_project/python_challenge

# you can rename the folder to use it your project
$ mv python_challenge my_project/ip_lookup

# Make sure the folder python_challenge/lookup/cache and its subfolders have permissions to read and write files
$ ls -l python_challenge/lookup/
$ ls -l python_challenge/lookup/cache

# Make sure the folder python_challenge/populate/test_data and its file have permissions to read files
$ ls -l python_challenge/populate/test_data
``` 
# How to Use
This tutorial assumes that you moved this project inside of your own project thas why all the import statements start with **python_challenge**.
## Populate
To populate all the GEO IP and RDAP data from IP's found in the test file preloaded by this project, just use it like this:
```python
from python_challenge.populate import populate

populate.populate()
```

To specifiy a file that you want to populate:
```python
from python_challenge.populate import populate

file_name = '/file_location/file.txt'
populate.populate(file_name=file_name)
```

By default the populate function uses cache to preload data that was already retrieved. If you need to get most up to date data, you can do it assigning **True** to parameter named **force_update_cache**:
```python
from python_challenge.populate import populate

file_name = '/file_location/file.txt'
populate.populate(file_name=file_name, force_update_cache=True)
```

## Geo IP Lookup
You can look for the GEO IP data from single IP address, it will return a dictionary:
```python
from python_challenge import lookup

geo_ip_dict = lookup.get_geo_ip_info(ip_address='244.36.171.60')
```

By default the get_geo_ip_info function uses cache . If you need to get most up to date data, you can do it assigning **True** to parameter named **force_update_cache**:
```python
from python_challenge import lookup

geo_ip_dict = lookup.get_geo_ip_info(ip_address='244.36.171.60', force_update_cache=True)
```

## RDAP Lookup
You can look for the RDAP data from single IP address, it will return a dictionary:
```python
from python_challenge import lookup

rdap_ip_dict = lookup.get_rdap_info(ip_address='244.36.171.60')
```

By default the get_rdap_info function uses cache . If you need to get most up to date data, you can do it assigning **True** to parameter named **force_update_cache**:
```python
from python_challenge import lookup

rdap_ip_dict = lookup.get_rdap_info(ip_address='244.36.171.60', force_update_cache=True)
```

## Query
You can perform queries in order to filter GEO IP and RDAP data previous populated.<br>
The queries are structured by using dictionaries and lists, some examples are  listed in order to understand how to create them:
### Single GEO IP query 
Create a main dictionary with only one key, this key will be the name of **field name** that is going to be look for in data.
<br><br>
The value for the **field name** has to be a dictionary with 2 keys **op** and **value**. The content from the **value** key will  be used to be compared with the operator defined in the content from **op** key.<br>
Check this example:

```python
from python_challenge.query import query

query_dict = {
    'ip': {
        'op': '=', 
        'value': '8.8.8.8'
    }
}
geo_ip_list = query.query_geo_ip(query_dict=query_dict))
```
The result will be a list filled by the data that matches the query.
<br><br>
The **op** key can receive these operators: **=**, **!=**, **>**, **<**, **>=**, **<=**, they can be compared with a single object from the **value** key. It can received also a **in** value, in this case the **value** key has to receive a list.

### Nested GEO IP query
You can create queries containing more than one filter, it supports **or** and **and** options, when you use one of this options as a key you have to assing a **list** as a value containing **single queries**.<br>
Check this example:
```python
from python_challenge.query import query

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
geo_ip_list = query.query_geo_ip(query_dict=query_dict))
```

### Single RDAP IP query 
It works the same was as the **Single GEO IP query**.
<br>
Check this example:
```python
from python_challenge.query import query

query_dict = {
    "country": {
        'op': '=',
        'value': 'JP'
    }
}
rdap_list = query.query_geo_ip(query_dict=query_dict))
```

### Nested RDAP IP query
It works the same was as the **Nested GEO IP query**.
<br>
Check this example:
```python
from python_challenge.query import query

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
rdap_list = query.query_geo_ip(query_dict=query_dict))
```

## Examples
It contains some examples that you can run in terminal by using the examples.py file.

Run to show the list of the examples available:
```bash
$ python3 examples.py --list-examples
```
Result:
```bash
test_populate_default_test_file
test_populate_from_file
test_populate_force_update_cache
test_get_geo_ip_info
test_get_rdap_info
test_get_geo_ip_info_force_update_cache
test_get_rdap_info_force_update_cache
test_single_geo_ip_query
test_nested_geo_ip_query
test_single_rdap_query
test_nested_rdap_query

```
<br>

Run a test:
```bash
# run a test passing input --run
$ python3 examples.py --run test_get_geo_ip_info
```
Result:
```bash
Retrieving GEO IP from 244.36.171.60
{   'city': '',
    'country_code': '',
    'country_name': '',
    'ip': '244.36.171.60',
    'latitude': 0,
    'longitude': 0,
    'metro_code': 0,
    'region_code': '',
    'region_name': '',
    'time_zone': '',
    'zip_code': ''}

```

<br>

If you want to save the result in a text file instead of being printed on the terminal, do it this way:
```bash
# run a test passing input --run and assign the file 
$ python3 examples.py --run test_get_geo_ip_info > /file_location/result.txt
```

# License
MIT License
