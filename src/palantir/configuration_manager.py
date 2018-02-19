"""A Class for manages a Palantir configuration file"""

from datetime import datetime

import yaml


def format_time_string(time_string):
    return datetime.strptime(time_string, '%d/%m/%Y')


class ConfigurationManager:
    """Represents a configuration file"""

    def __init__(self, configuration_filepath):
        self.config = {}

        with open(configuration_filepath) as yaml_file:
            cfg = yaml.load(yaml_file)

        # description
        description = cfg['description']
        self.config['start date'] = format_time_string(description['start date'])

        # defaults
        well_defaults = cfg['defaults']['well']
        self.config['choke'] = well_defaults['choke']
        self.config['active period'] = well_defaults['active period']
        self.config['ultimate oil recovery'] = well_defaults['oil well']['ultimate oil recovery']
        self.config['initial oil rate'] = well_defaults['oil well']['initial oil rate']
        self.config['gas oil ratio'] = well_defaults['oil well']['gas oil ratio']
        self.config['b oil'] = well_defaults['oil well']['b oil']
        self.config['ultimate gas recovery'] = well_defaults['gas well']['ultimate gas recovery']
        self.config['initial gas rate'] = well_defaults['gas well']['initial gas rate']
        self.config['gas condensate ratio'] = well_defaults['gas well']['gas condensate ratio']
        self.config['b gas'] = well_defaults['gas well']['b gas']

        # facilities
        facilities = cfg['facilities']
        self.config['asset'] = facilities['asset']
        self.config['pexes'] = facilities['pexes']

        # programs
        if 'programs' in cfg:
            self.config['programs'] = cfg['programs']
