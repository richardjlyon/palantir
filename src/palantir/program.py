"""Classes that represent a Rig and associated rig Program"""
from datetime import datetime


class Rig:
    """Represents a drilling rig"""

    def __init__(self, name=None):
        self.name = name
        self.program = Program()


class Program:
    """Represents a rig program"""

    def __init__(self):
        self.start_date = None
        self.elapsed_time = None
        self.steps = []

    def add_step(self, step):
        step.program = self
        self.steps.append(step)

    def execute(self):
        [step.execute() for step in self.steps]


class Step:
    def __init__(self, name=None):
        self.name = name
        self.program = None

    def execute(self):
        raise NotImplementedError


class StartStep(Step):

    def __init__(self, start_date=None, location=None, parameters=None):
        super().__init__()
        self.start_date = start_date
        self.location = location

        if parameters:
            date_string, wellhead_platform_name = parameters.split(',')
            self.start_date = datetime.strptime(date_string, "%d/%m/%Y")
            self.location = wellhead_platform_name  # TODO fix this

    def execute(self):
        self.program.start_date = self.start_date
        self.program.location = self.location
        self.program.elapsed_time = 0

    def __str__(self):
        return "START: {}, {}".format(self.start_date, self.location)


class MoveStep(Step):

    def __init__(self, destination=None, duration=None, parameters=None):
        self.destination = destination
        self.duration = duration

        if parameters:
            wellhead_platform_name, duration = parameters.split(',')
            self.destination = wellhead_platform_name
            self.duration = int(duration)

    def execute(self):
        self.program.location = self.destination
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "MOVE: {}, {}".format(self.destination, self.duration)


class StandbyStep(Step):

    def __init__(self, duration=None, parameters=None):
        self.duration = duration

        if parameters:
            self.duration = duration

    def execute(self):
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "STANDBY: {}".format(self.duration)


class DrillStep(Step):

    def __init__(self, well=None, duration=None, parameters=None):  # TODO make this a default setting
        self.well = well
        self.duration = duration

        if parameters:
            well_name, duration = parameters.split(',')
            self.well = well_name
            self.duration = duration

    def execute(self):
        self.program.location.add_well(self.well)
        self.program.elapsed_time += self.duration

    def __str__(self):
        return "DRILL: {}, {}".format(self.well, self.duration)
