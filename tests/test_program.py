from datetime import datetime

from palantir.facilities import GasWell, OilWell, WellHeadPlatform
from palantir.program import Program, Rig


class TestProgram:

    def test_basic(self, program_steps):
        program = program_steps.programs[0]
        assert isinstance(program, Program)

    def test_rig(self, program_steps):
        program = program_steps.programs[0]
        assert isinstance(program.rig, Rig)


class TestSteps:
    def test_start_step(self, program_steps):
        program = program_steps.programs[0]

        # start: 01/01/2018, AEP
        step0 = program.steps[0]
        step0.execute()

        assert step0.elapsed_time == 0
        assert program.elapsed_time == 0
        assert program.start_date == datetime(2018, 1, 1)
        assert isinstance(program.rig.location, WellHeadPlatform)
        assert program.rig.location.name == 'AEP'

        # drill: NNM-7, oil, 70
        step1 = program.steps[1]
        step1.execute()
        well = program.asset.get_well_by_name('NNM-7')

        assert step1.elapsed_time == 0
        assert program.elapsed_time == 70
        assert isinstance(well, OilWell)
        assert well.start_date == datetime(2018, 1, 1)

        # move: WHP4, 30
        step2 = program.steps[2]
        step2.execute()

        assert step2.elapsed_time == 70
        assert program.elapsed_time == 100
        assert program.rig.location.name == 'WHP4'

        # drill: NNM-402, gas, 70
        step3 = program.steps[3]
        step3.execute()
        well = program.asset.get_well_by_name('NNM-402')

        assert step3.elapsed_time == 100
        assert program.elapsed_time == 170
        assert isinstance(well, GasWell)
        assert well.start_date == datetime(2018, 4, 11)

        # standby: 100
        step4 = program.steps[4]
        step4.execute()

        assert step4.elapsed_time == 170
        assert program.elapsed_time == 270
