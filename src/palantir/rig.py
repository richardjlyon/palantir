"""Classes that represent a Rig and associated rig Program"""


# TODO add parameter checking to steps

class Rig:
    """Represents a drilling rig"""

    def __init__(self, name=None):
        self.name = name


class Program:
    """Represents a rig program"""

    def __init__(self, rig):
        self.rig = rig
        self.start_date = None
        self.elapsed_time = None
        self.location = None
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

    def __init__(self, start_date=None, location=None):
        super().__init__()
        self.start_date = start_date
        self.location = location

    def execute(self):
        self.program.start_date = self.start_date
        self.program.location = self.location
        self.program.elapsed_time = 0


class MoveStep(Step):

    def __init__(self, destination=None, duration=None):
        self.destination = destination
        self.duration = duration

    def execute(self):
        self.program.location = self.destination
        self.program.elapsed_time += self.duration


class StandbyStep(Step):

    def __init__(self, duration=None):
        self.duration = duration

    def execute(self):
        self.program.elapsed_time += self.duration


class DrillStep(Step):

    def __init__(self, well=None, duration=None):  # TODO make this a default setting
        self.well = well
        self.duration = duration

    def execute(self):
        self.program.location.add_well(self.well)
        self.program.elapsed_time += self.duration
