"""Classes that represent a Rig and associated rig Program"""
from datetime import datetime, timedelta

from palantir.facilities import GasWell, OilWell


class Rig:
    """Represents a drilling rig"""

    def __init__(self, name=None):
        self.name = name
        self.location = None


class Program:
    """Represents a rig program"""

    def __init__(self, asset=None, config=None, rig_name=None, steps=None):
        self.asset = asset
        self.config = config
        self.rig = Rig(name=rig_name)
        self.start_date = None
        self.elapsed_time = None
        self.steps = []

        self._parse_program_steps(steps)

    def _parse_program_steps(self, steps):
        commands = {
            'start': StartStep,
            'move': MoveStep,
            'drill': DrillStep,
            'standby': StandbyStep
        }

        for step in steps:
            elements = list(step.items())[0]
            action = elements[0].lower()  # 'start'
            parameters = elements[1]  # '01/01/2018'

            step = commands[action](parameters=parameters, program=self)
            self.add_step(step)

    def add_step(self, step):
        self.steps.append(step)

    def execute(self):
        [step.execute() for step in self.steps]


def get_parameters(string):
    if ',' in string:
        return (param.strip() for param in string.split(','))
    else:
        return string.strip()


class Step:
    def __init__(self, program=None):
        self.asset = None
        self.program = program
        self.elapsed_time = None

    def execute(self):
        raise NotImplementedError


# TODO refactor parameter setting

class StartStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__(program=program)
        self.start_date = None
        self.location = None

        if parameters:
            date_string, wellhead_platform_name = get_parameters(parameters)
            self.start_date = datetime.strptime(date_string, "%d/%m/%Y")
            self.location = wellhead_platform_name

    def execute(self):
        self.elapsed_time = 0
        self.program.elapsed_time = 0
        self.program.start_date = self.start_date
        self.program.rig.location = self.program.asset.get_wellhead_platform_by_name(self.location)

    def __str__(self):
        return "START: {}, {}".format(self.start_date, self.location)


class DrillStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__(program=program)
        self.well_name = None
        self.type = None
        self.duration = None

        if parameters:
            well_name, type, duration = get_parameters(parameters)
            self.well_name = well_name
            self.type = type
            self.duration = int(duration)

    def execute(self):

        self.elapsed_time = self.program.elapsed_time
        well_start_date = self.program.start_date + timedelta(days=self.elapsed_time)

        if self.type == 'oil':
            well = OilWell(name=self.well_name, start_date=well_start_date, well_defaults=self.program.config)
        else:
            well = GasWell(name=self.well_name, start_date=well_start_date, well_defaults=self.program.config)
        self.program.rig.location.add_well(well)
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "DRILL: {}, {}, {}".format(self.well_name, self.type, self.duration)


class MoveStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__(program=program)
        self.destination = None
        self.duration = None

        if parameters:
            wellhead_platform_name, duration = get_parameters(parameters)
            self.destination = wellhead_platform_name
            self.duration = int(duration)

    def execute(self):
        self.elapsed_time = self.program.elapsed_time
        self.program.rig.location = self.program.asset.get_wellhead_platform_by_name(self.destination)
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "MOVE: {}, {}".format(self.destination, self.duration)


class StandbyStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__(program=program)
        self.duration = None

        if parameters:
            self.duration = int(parameters)

    def execute(self):
        self.elapsed_time = self.program.elapsed_time
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "STANDBY: {}".format(self.duration)
