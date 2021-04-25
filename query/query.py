import json
import os
from pathlib import Path
import copy

from lookup import geo_ip, rdap


def query_geo_ip(query_dict: dict) -> list:
    """
    Receives a dict with the query with the 
    data that wants to be filter.
    """
    results = []
    finder = Finder()
    pathlist = Path(geo_ip.geo_ip_info_cache_directory()).glob('*.json')
    for path in pathlist:
        path_in_str = str(path)
        if os.path.isfile(path_in_str):
            with open(path_in_str, 'r') as json_file:
                json_data = json.load(json_file)
                query_result = finder.execute_search(json_data, query_dict)
                if query_result:
                    results.append(json_data)

    return results


def query_rdap(query_dict: dict) -> list:
    """
    Receives a dict with the query with the 
    data that wants to be filter.
    """
    results = []
    finder = Finder()
    pathlist = Path(rdap.rdap_info_cache_directory()).glob('*.json')
    for path in pathlist:
        path_in_str = str(path)
        if os.path.isfile(path_in_str):
            with open(path_in_str, 'r') as json_file:
                json_data = json.load(json_file)
                query_result = finder.execute_search(json_data, query_dict)
                if query_result:
                    results.append(json_data)

    return results


class Finder:
    """
    Evaluates queries to check if they match with the data.
    """

    def __init__(self):
        self._query_results = {}
        self._data = {}

    def execute_search(self, data: dict, query: dict) -> bool:
        """
        Main method to evaluate if a data dict
        contains all the query filters declared.
        """
        # it creates a copy from the query so it can replace
        # the result from the search in the key from the field
        # names
        self._query_results = copy.deepcopy(query)
        # asigns data to an atribute so it can be accesed in any
        # method.
        self._data = data

        self._iterate_query(query, self._query_results)

        return self._evaluate_query_results()

    def _iterate_query(self, query, query_results):
        """
        Checks every option on the evaluator query
        """
        if isinstance(query, dict):
            if 'and' in query or 'or' in query:
                # if key is "and" or "or" is expected to get only one element
                key, obj = list(query.items())[0]
                if hasattr(obj, '__iter__') and not isinstance(obj, str):
                    for index, item in enumerate(obj):
                        self._iterate_query(
                            query=item,
                            query_results=query_results[key][index]
                        )
                else:
                    print(
                        f'key "{key}" is expected to have an interable object')
            else:
                # only one value expected
                key, obj = list(query.items())[0]
                evaluator_result = self._eval_op_value_dict(key, the_dict=obj)
                # changes the original value for bool result
                query_results[key] = evaluator_result

    def _eval_op_value_dict(self, key: str, the_dict: dict) -> bool:
        """
        Get the value from the key that want to 
        be compared.
        """
        if isinstance(the_dict, dict):
            if 'op' in the_dict and 'value' in the_dict:
                value_from_data = self._get_value_by_key_in_data(
                    data=self._data,
                    key_name=key
                )
                evaluator_result = self._operator_evaluator(
                    item_value=value_from_data,
                    operator=the_dict['op'],
                    search_value=the_dict['value']
                )
                return evaluator_result
            else:
                print(f'key "{key}" is expected to have an interable object')
        else:
            print(the_dict, ': dict has to have a the keys "op" and "value"')

    def _get_value_by_key_in_data(self, data, key_name) -> object:
        """
        Searches for a key in data.
        if found returns the value
        """
        if isinstance(data, dict):
            if key_name in data:
                return data[key_name]
        elif hasattr(data, '__iter__') and not isinstance(data, str):
            for datum in data:
                self._get_value_by_key_in_data(
                    data=datum,
                    key_name=key_name
                )

        return ''

    def _operator_evaluator(self, item_value, operator, search_value) -> bool:
        """
        Perfoms the evaluations
        """
        if operator == '=':
            return item_value == search_value
        elif operator == '!=':
            return item_value != search_value
        elif operator == 'in' and search_value is not None and hasattr(search_value, '__iter__'):
            return item_value in search_value
        elif (item_value is not None and search_value is not None
              and type(item_value) is type(search_value)):
            if operator == '>':
                return item_value > search_value
            elif operator == '<':
                return item_value < search_value
            elif operator == '>=':
                return item_value >= search_value
            elif operator == '<=':
                return item_value <= search_value

        return False

    def _evaluate_query_results(self) -> bool:
        """
        Evaluates the string conditions return by _do_evaluation_query_results
        """
        str_result = self._do_evaluation_query_results(self._query_results)

        return eval(str_result)

    def _do_evaluation_query_results(self, the_dict: dict) -> str:
        """
        It will receive something like this:
        {'and': [{'country_name': True}, {'region_name': False}, 
        {'or': [{'metro_code': True}, {'metro_code': False}]}]}

        It will return string values like these examples:
        Single Query: ( True )
        Nested Query: ( True or False ( True and False) )
        """
        if 'or' in the_dict or 'and' in the_dict:
            key, lst = list(the_dict.items())[0]
            result = f' {key} '.join(
                [self._do_evaluation_query_results(item) for item in lst]
            )
            return f'( {result} )'

        # if it is a single value
        key, result = list(the_dict.items())[0]
        return str(result)
