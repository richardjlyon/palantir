from datetime import datetime

from palantir.program import Program


# # Make a simple asset
# asset = Asset(name="MXII")
# pex = Pex(name='Nene')
# whp3 = WellHeadPlatform(name='WHP3')
# whp4 = WellHeadPlatform(name='WHP4')
# asset.add_pex(pex)
# pex.add_wellhead_platform(whp3)
# pex.add_wellhead_platform(whp4)
#
# rig = Rig()
#
# program = Program()
# program.asset = asset
# program.rig = rig

# start_step = StartStep(parameters="01/01/2018, WHP3")
# drill_step = DrillStep(parameters="NNM-405, 70")
# move_step = MoveStep(parameters="WHP4, 30")
# standby_step = StandbyStep(parameters="100")


class xxxTestStep:

    def test_steps(self):
        # global start_step, move_step, drill_step, standby_step
        # assert start_step.start_date == datetime(2018,1,1)
        # assert start_step.location == 'WHP3'
        # assert move_step.destination == 'WHP4'
        # assert move_step.duration == 30
        # assert drill_step.well == 'NNM-405'
        # assert drill_step.duration == 70
        # assert standby_step.duration == 100
        pass


class TestProgram:

    def test_program_initialisation(self):
        # GIVEN a new program
        # WHEN elapsed time is retrieved
        # THEN elapsed time is 0
        program = Program()
        assert program.elapsed_time == None

    def test_program(self, manager_test_program):
        program = manager_test_program.programs[0]
        program.execute()

        assert program.start_date == datetime(2018, 1, 1)


class XXXTestRig:

    def test_rig_has_name(self, manager_test_program):
        rig = manager_test_program.programs[0].rig
        assert rig.name == 'Rig1'
