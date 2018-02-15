from datetime import datetime

from palantir.facilities import Well, WellHeadPlatform
from palantir.rig import DrillStep, MoveStep, Program, Rig, StandbyStep, StartStep

rig = Rig('Sapphire')
program = Program(rig=rig)
whp3 = WellHeadPlatform(name="WHP3")
whp4 = WellHeadPlatform(name="WHP4")
nnm401 = Well(name="NNM-401")

start_step = StartStep(start_date=datetime(2018, 1, 1), location=whp3)
move_step = MoveStep(destination=whp4, duration=30)
standby_step = StandbyStep(duration=45)
drill_step = DrillStep(well=nnm401, duration=70)


class TestRig:

    def test_name(self):
        global rig
        assert rig.name == 'Sapphire'


class TestProgram:

    def test_start(self):
        # GIVEN a program
        # WHEN I issue a 'start' action
        # the program start date is set
        global program, start_step
        program.add_step(start_step)
        program.execute()
        assert program.start_date == datetime(2018, 1, 1)
        assert program.location == whp3
        assert program.elapsed_time == 0

    def test_move_step(self):
        global program, start_step, move_step
        program.add_step(start_step)
        program.add_step(move_step)
        program.execute()
        assert program.location == whp4
        assert program.elapsed_time == 30

    def test_standby_step(self):
        global program, start_step, move_step, standby_step
        program.add_step(start_step)
        program.add_step(move_step)
        program.add_step(standby_step)
        program.execute()
        assert program.location == whp4
        assert program.elapsed_time == 75

    def test_drill_step(self):
        global program, start_step, move_step, standby_step, drill_step, whp4
        program.add_step(start_step)
        program.add_step(move_step)
        program.add_step(standby_step)
        program.add_step(drill_step)
        program.execute()
        assert program.elapsed_time == 145
        assert whp4.wells[0].name == 'NNM-401'
