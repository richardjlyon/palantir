import pytest
from palantir import make_temp_file
from palantir.facilities import Asset
from palantir.manager import ConfigurationFile, Manager

# TODO move this to conftest.py
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
def simple_config():
    global simple
    configuration_file = make_temp_file(simple)
    c = ConfigurationFile(configuration_file.name)
    yield c.yaml
    configuration_file.close()


@pytest.fixture()
def manager():
    global simple
    configuration_file = make_temp_file(simple)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()


class TestInitialiseDefaults:

    def test_initialise_defaults(self, manager):
        assert manager.defaults['choke'] == 100
        assert manager.defaults['gas oil ratio'] == [2000, 4000]


class TestInitialiseAsset:

    def test_initialise_asset(self, manager):
        assert isinstance(manager.asset, Asset)

    def test_initialise_pexes(self, manager):
        assert len(manager.asset.pexes) == 2

    def test_initialise_wellhead_platforms(self, manager):
        assert len(manager.asset.pexes[0].wellhead_platforms) == 3

    def test_inititalise_wells(self, manager):
        assert len(manager.asset.pexes[0].wellhead_platforms[0].wells) == 3
        # print(RenderTree(manager.asset))

    def test_oil_well_defaults(self, manager):
        nnm3 = manager.asset.pexes[0].wellhead_platforms[0].wells[0]
        assert nnm3.active_period == 3650
        assert nnm3.choke == 100
        assert nnm3.ultimate_oil_recovery == 8000000
        assert nnm3.initial_oil_rate == 5000
        assert nnm3.gas_oil_ratio == [2000, 4000]
        assert nnm3.b_oil == 1.0

    # @pytest.mark.skip(reason="not implemented a gas well yet")
    def test_gas_well_defaults(self, manager):
        ljm11 = manager.asset.pexes[1].wellhead_platforms[0].wells[0]
        assert ljm11.active_period == 3650
        assert ljm11.choke == 100
        assert ljm11.ultimate_gas_recovery == 0
        assert ljm11.initial_gas_rate == 0
        assert ljm11.gas_condensate_ratio == 0
        assert ljm11.b_gas == 0

    def test_existing_oil_well(self, manager):
        # GIVEN an existing producing oil well
        # WHEN getting its paramters
        # THEN return the parameters from the config file
        nnm3 = manager.asset.pexes[0].wellhead_platforms[0].wells[0]
        assert nnm3.oil_rate == 1851
        assert nnm3.oil_cumulative == 2846703
        assert nnm3.gas_rate == 2072000
        assert nnm3.gas_cumulative == 4845154174

    def test_exisiting_gas_well(self, manager):
        ljm11 = manager.asset.pexes[1].wellhead_platforms[0].wells[0]
        assert ljm11.condensate_rate == 1234
        assert ljm11.condensate_cumulative == 987654
        assert ljm11.gas_rate == 31415927
        assert ljm11.gas_cumulative == 533919437


class TestRunProgram:

    def test_rig(self, manager):
        rig = manager.rigs[0]
        assert rig.name == 'Rig1'


class TestConfigurationFile:

    def test_get_sections(self, simple_config):
        # GIVEN a configuration file
        # WHEN a top level section is requested
        # THEN return a dictionary
        assert isinstance(simple_config['defaults'], dict)

    def test_get_options(self, simple_config):
        # GIVEN a section from a configuration file
        # WHEN an option is requested
        # THEN return a string, integer, list, and date
        assert isinstance(simple_config['defaults']['well']['choke'], int)

# class TestProgram:
#
#     def test_program_has_programs(self, manager_test_program):
#         # TODO put this in test_manager :)
#         assert len(manager_test_program.programs) > 0
#         assert isinstance(manager_test_program.programs[0], Program)
#
#     def test_program_has_rig(self, manager_test_program):
#         program = manager_test_program.programs[0]
#         assert isinstance(program.rig, Rig)
