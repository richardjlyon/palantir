"""Classes for parsing a configuration file and managing the creation of a forecast"""

from palantir.configuration_manager import ConfigurationManager
from palantir.facilities import Asset, GasWell, OilWell, Pex, WellHeadPlatform
from palantir.program import Program


class Manager:
    """Manages the production and exporting of a forecast"""

    def __init__(self, configuration_filepath):

        configuration_manager = ConfigurationManager(configuration_filepath)
        self.config = configuration_manager.config

        self.asset = None
        self.programs = []
        self.rig = None
        self.profiles = None

        self._initialise_facilities()
        self._run_programs()

    def _initialise_facilities(self):
        self.asset = Asset(self.config['asset'], defaults=self.config)

        for pex_name, whps in self.config['pexes'].items():
            pex = Pex(name=pex_name)
            self.asset.add_pex(pex)

            for whp_name, wells in whps.items():
                whp = WellHeadPlatform(name=whp_name)
                pex.add_wellhead_platform(whp)

                for well_name, well_details in wells.items():
                    if well_details['type'] == 'oil':
                        well = OilWell(name=well_name, well_details=well_details, defaults=self.config)
                    else:
                        well = GasWell(name=well_name, well_details=well_details, defaults=self.config)
                    whp.add_well(well)

    def _run_programs(self):
        """Parses configuration file for program steps, builds, and runs the program"""
        # TODO process multiple programs
        # TODO trap no program
        # TODO get WellheadPlatform and Well objects, not names
        # TODO check WellheadPlatform exists and create if missing

        if 'programs' in self.config:
            programs = self.config['programs']

            for rig_name, program_details in programs.items():
                program = Program(rig_name=rig_name, steps=program_details['program'])
                self.programs.append(program)
