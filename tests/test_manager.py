from palantir.facilities import Asset, Pex, WellHeadPlatform, Well
from palantir.program import Program

class TestInitialise:

    def test_initialise_defaults(self,manager):
        assert isinstance(manager.defaults, dict)

    def test_initialise_asset(self, manager):
        assert isinstance(manager.asset, Asset)

    def test_run_programs(self, manager):
        assert isinstance(manager.programs, list)
        assert isinstance(manager.programs[0], Program)

class TestDefaults:

    def test_choke(self, manager):
        assert manager.defaults['choke'] == 100

