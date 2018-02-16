"""Classes that represent a Rig and associated rig Program"""
from datetime import datetime, timedelta


class Rig:
    """Represents a drilling rig"""

    def __init__(self, name=None):
        self.name = name
        self.program = Program()


class Program:
    """Represents a rig program"""

    def __init__(self):
        self.rig = None
        self.asset = None
        self.start_date = None
        self.elapsed_time = None
        self.steps = []

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
    def __init__(self, name=None):
        self.name = name  # TODO what's this?
        self.elapsed_time = None
        self.asset = None
        self._program = None

    def execute(self):
        raise NotImplementedError


# TODO refactor parameter setting

class StartStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__()
        self.program = program
        self.start_date = None
        self.location = None

        if parameters:
            date_string, wellhead_platform_name = get_parameters(parameters)
            self.start_date = datetime.strptime(date_string, "%d/%m/%Y")
            whp = self.asset
            self.location = wellhead_platform_name  # TODO fix this

    def execute(self):
        self.program.elapsed_time = 0
        self.elapsed_time = 0
        self.program.start_date = self.start_date
        self.program.location = self.location

    def __str__(self):
        return "START: {}, {}".format(self.start_date, self.location)


class DrillStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__()
        self.program = program
        self.well = None
        self.duration = None

        if parameters:
            well_name, duration = get_parameters(parameters)
            self.well = well_name
            self.duration = int(duration)

    def execute(self):
        self.elapsed_time = self.program.elapsed_time
        well_start_date = self.program.start_date + timedelta(days=self.elapsed_time)
        self.program.location.add_well(self.well)
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "DRILL: {}, {}".format(self.well, self.duration)


class MoveStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__()
        self.program = program
        self.destination = None
        self.duration = None

        if parameters:
            wellhead_platform_name, duration = get_parameters(parameters)
            self.destination = wellhead_platform_name
            self.duration = int(duration)

    def execute(self):
        self.program.location = self.destination
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "MOVE: {}, {}".format(self.destination, self.duration)


class StandbyStep(Step):

    def __init__(self, parameters=None, program=None):
        super().__init__()
        self.program = program
        self.duration = None

        if parameters:
            self.duration = int(parameters)

    def execute(self):
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "STANDBY: {}".format(self.duration)
