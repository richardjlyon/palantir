"""Classes for parsing a configuration file and managing the creation of a forecast"""
import re
from datetime import datetime

import yaml
from palantir.facilities import Asset, GasWell, OilWell, Pex, WellHeadPlatform
from palantir.program import DrillStep, MoveStep, Program, Rig, StandbyStep, StartStep


def validate(value):
    """Do basic error checking and typecasting on value"""
    result = value
    if isinstance(value, str):
        match = re.search(r'(\d+/\d+/\d+)', str(value))
        if match:
            result = datetime.strptime(value, "%d/%m/%Y")
    return result


class Manager:
    """Manages the production and exporting of a forecast"""

    def __init__(self, configuration_filepath):
        self.defaults = {}
        self.asset = None
        self.programs = []
        self.profiles = None
        self._config = None  # TODO remove this - should be defaults

        self._initialise_defaults(configuration_filepath)
        self._initialise_asset()
        self._run_programs()

    def _initialise_defaults(self, configuration_filepath):
        self._config = ConfigurationFile(configuration_filepath).yaml
        well_defaults = self._config['defaults']['well']
        self.defaults['choke'] = well_defaults['choke']
        self.defaults['active period'] = well_defaults['active period']
        self.defaults['ultimate oil recovery'] = well_defaults['oil well']['ultimate oil recovery']
        self.defaults['initial oil rate'] = well_defaults['oil well']['initial oil rate']
        self.defaults['gas oil ratio'] = well_defaults['oil well']['gas oil ratio']
        self.defaults['b oil'] = well_defaults['oil well']['b oil']
        self.defaults['ultimate gas recovery'] = well_defaults['gas well']['ultimate gas recovery']
        self.defaults['initial gas rate'] = well_defaults['gas well']['initial gas rate']
        self.defaults['gas condensate ratio'] = well_defaults['gas well']['gas condensate ratio']
        self.defaults['b gas'] = well_defaults['gas well']['b gas']

    def _initialise_asset(self):
        facilities = self._config['facilities']
        self.asset = Asset(name=facilities['asset'], defaults=self.defaults)

        for pex_name, whps in facilities['pexes'].items():
            pex = Pex(name=pex_name)
            self.asset.add_pex(pex)

            for whp_name, wells in whps.items():
                whp = WellHeadPlatform(name=whp_name)
                pex.add_wellhead_platform(whp)

                for well_name, well_details in wells.items():
                    if well_details['type'] == 'oil':
                        well = OilWell(name=well_name, well_details=well_details, defaults=self.defaults)
                    else:
                        well = GasWell(name=well_name, well_details=well_details, defaults=self.defaults)
                    whp.add_well(well)

    def _run_programs(self):
        """Parses configuration file for program steps, builds, and runs the program"""
        # TODO process multiple programs
        # TODO trap no program
        # TODO get WellheadPlatform and Well objects, not names
        # TODO check WellheadPlatform exists and create if missing

        commands = {
            'start': StartStep,
            'move': MoveStep,
            'drill': DrillStep,
            'standby': StandbyStep
        }

        programs = self._config['programs']

        for rig_name, program_details in programs.items():

            program = Program()
            program.rig = Rig(name=rig_name)

            program_steps = program_details['program']
            for step in program_steps:
                elements = list(step.items())[0]
                action = elements[0].lower()  # 'start'
                parameters = elements[1]  # '01/01/2018'

                step = commands[action](parameters=parameters)
                program.add_step(step)


class ConfigurationFile:
    """Represents a configuration file"""

    def __init__(self, configuration_filepath):
        self.yaml = None
        self._parse_configuration(configuration_filepath)

    def _parse_configuration(self, configuration_filepath):
        with open(configuration_filepath) as yaml_file:
            self.yaml = yaml.load(yaml_file)
