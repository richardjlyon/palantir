"""A Class for manages a Palantir configuration file"""
import re
from collections.abc import Mapping
from datetime import datetime

import yaml


def _is_date(self, string):
    result = string
    if isinstance(string, str):
        match = re.search(r'(\d+/\d+/\d+)', str(string))
        if match:
            result = datetime.strptime(string, "%d/%m/%Y")
    return result


class ConfigurationManager(Mapping):
    """Managers accessing a configuration file
       See: http://www.kr41.net/2016/03-23-dont_inherit_python_builtin_dict_type.html
    """

    def __init__(self, configuration_filepath):
        with open(configuration_filepath) as yaml_file:
            self._storage = yaml.load(yaml_file)

    def __getitem__(self, key):
        if key in self._storage:
            return self._storage[key]
        else:
            return None

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)
