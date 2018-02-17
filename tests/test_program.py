from datetime import datetime

from palantir.facilities import WellHeadPlatform
from palantir.program import Program, Rig


class TestProgram:

    def test_basic(self, program_step_1):
        program = program_step_1.programs[0]
        assert isinstance(program, Program)

    def test_rig(self, program_step_1):
        program = program_step_1.programs[0]
        assert isinstance(program.rig, Rig)


class TestStartStep:
    def test_steps(self, program_step_1):
        program = program_step_1.programs[0]
        step = program.steps[0]
        program.execute()
        assert step.elapsed_time == 0
        assert program.elapsed_time == 0
        assert program.start_date == datetime(2018, 1, 1)
        assert isinstance(program.location, WellHeadPlatform)
        assert program.location.name == 'AEP'
