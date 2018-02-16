from datetime import datetime

import pytest
from palantir.facilities import Well, WellHeadPlatform
from palantir.program import DrillStep, MoveStep, Program, Rig, StandbyStep, StartStep

simple = '''
defaults:
    well:
        choke: 100
        active period: 3650 # days
        oil well:
            ultimate oil recovery: 8000000
            initial oil rate: 5000
            gas oil ratio: [2000, 4000]
            b oil: 1.0
        gas well:
            ultimate gas recovery: 0
            initial gas rate: 0
            gas condensate ratio: 0
            b gas: 0
facilities:
    asset: MXII
    pexes:
        Nene:
            AEP:
                NNM-3:
                    type: oil
                    oil rate: 1851
                    oil cumulative: 2846703
                    gas rate: 2072000
                    gas cumulative: 4845154174
                NNM-5:
                    type: oil
                    oil rate: 198
                    oil cumulative: 458645
                    gas rate: 197634
                    gas cumulative: 458638676
                NNM-6:
                    type: oil
                    oil rate: 1964
                    oil cumulative: 2051240
                    gas rate: 8963974
                    gas cumulative: 7378218973
            WHP4:
                NNM-401:
                    type: oil
                    oil rate: 4000
                    oil cumulative: 507833
                    gas rate: 16000000
                    gas cumulative: 1313829371
                NNM-402:
                    type: oil
                    oil rate: 1011
                    oil cumulative: 444514
                    gas rate: 4074000
                    gas cumulative: 1720575712
                NNM-403:
                    type: oil
                    oil rate: 2943
                    oil cumulative: 639181
                    gas rate: 12942758
                    gas cumulative: 3289178468
                NNM-404:
                    type: oil
                    oil rate: 3924
                    oil cumulative: 648415
                    gas rate: 7923678
                    gas cumulative: 1468394590
            WHP3:
                NNM-301:
                    type: oil
                    oil rate: 2899
                    oil cumulative: 667239
                    gas rate: 6899247
                    gas cumulative: 1479210651
                NNM-302:
                    type: oil
                    oil rate: 2943
                    oil cumulative: 433918
                    gas rate: 2942759
                    gas cumulative: 433919437
                NNM-303:
                    type: oil
                    oil rate: 1947
                    oil cumulative: 279266
                    gas rate: 3947336
                    gas cumulative: 507266010
                NNM-304:
                    type: oil
                    oil rate: 1556
                    oil cumulative: 108577
                    gas rate: 0
                    gas cumulative: 0
        Litchendjili:
            LTC1:
                LJM-11:
                    type: gas
                    condensate rate: 1234
                    condensate cumulative: 987654
                    gas rate: 31415927
                    gas cumulative: 533919437
drilling:
    Rig1:
        program:
            - start: 01/01/2018, WHP3
            - drill: NNM-305, 70
            - drill: NNM-306, 70
            - move: WHP4, 30
            - drill: NNM-405, 70
            - drill: NNM-406, 70
            - move: WHPL1, 30
            - drill: L14, 70
            - drill: L15, 70
            - standby: 100
    '''


@pytest.fixture()
def manager():
    global simple
    configuration_file = make_temp_file(simple)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()


rig = Rig('Sapphire')
program = Program()
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
        # assert whp4.wells[0].name == 'NNM-401'
