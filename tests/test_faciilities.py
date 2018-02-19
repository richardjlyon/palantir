from datetime import datetime

import pytest
from palantir.facilities import Asset, OilWell, Pex, WellHeadPlatform


class TestAsset:

    def test_name(self, manager):
        assert manager.asset.name == 'MXII'

    def test_pexes(self, manager):
        assert len(manager.asset.pexes) == 2
        assert isinstance(manager.asset.pexes[0], Pex)

    def test_wellhead_platforms(self, manager):
        assert len(manager.asset.wellhead_platforms) == 4
        assert isinstance(manager.asset.wellhead_platforms[0], WellHeadPlatform)

    def test_wells(self, manager):
        assert len(manager.asset.wells) == 12
        assert isinstance(manager.asset.wells[0], OilWell)

    def test_get_wellhead_platform_by_name(self, manager):
        whp = manager.asset.get_wellhead_platform_by_name('WHP4')
        assert isinstance(whp, WellHeadPlatform)
        assert whp.name == 'WHP4'

    def test_get_well_by_name(self, manager):
        well = manager.asset.get_well_by_name('NNM-402')
        assert isinstance(well, OilWell)
        assert well.name == 'NNM-402'

    def test_add_pex(self, manager):
        pex_count = len(manager.asset.pexes)
        pex = Pex(name='New Pex')
        manager.asset.add_pex(pex)
        assert len(manager.asset.pexes) == pex_count + 1

    def test_exception_adding_non_pex(self, manager):
        with pytest.raises(ValueError):
            manager.asset.add_pex('Not a Pex')


class TestPex:

    def test_name(self, manager):
        assert manager.asset.pexes[0].name == 'Nene'

    def test_parent(self, manager):
        assert isinstance(manager.asset.pexes[0].parent, Asset)

    def test_wellhead_platforms(self, manager):
        assert len(manager.asset.pexes[0].wellhead_platforms) == 3
        assert isinstance(manager.asset.pexes[0].wellhead_platforms[0], WellHeadPlatform)

    def test_add_wellhead_platform(self, manager):
        wellhead_platform_count = len(manager.asset.pexes[0].wellhead_platforms)
        whp = WellHeadPlatform(name='New Wellhead Platform')
        manager.asset.pexes[0].add_wellhead_platform(whp)
        assert len(manager.asset.pexes[0].wellhead_platforms) == wellhead_platform_count + 1

    def test_exception_adding_non_whp(self, manager):
        with pytest.raises(ValueError):
            manager.asset.pexes[0].add_wellhead_platform('Not a Wellhead Platform')


class TestWellheadPlatform:

    def test_name(self, manager):
        assert manager.asset.pexes[0].wellhead_platforms[0].name == 'AEP'

    def test_parent(self, manager):
        assert isinstance(manager.asset.pexes[0].wellhead_platforms[0].parent, Pex)

    def test_wells(self, manager):
        assert len(manager.asset.pexes[0].wellhead_platforms[0].wells) == 3

    def test_remaining_slots(self, manager):
        assert manager.asset.pexes[0].wellhead_platforms[0].remaining_slots == 3

    def test_add_well(self, manager):
        config = {
            'start date': datetime.now(),
            'active period': None,
            'choke': None,
            'ultimate oil recovery': None,
            'initial oil rate': None,
            'gas oil ratio': None,
            'b oil': None}
        well_details = {
            'oil rate': None,
            'oil cumulative': None,
            'gas rate': None,
            'gas cumulative': None
        }
        whp = manager.asset.pexes[0].wellhead_platforms[0]
        well_count = len(whp.wells)
        well = OilWell(name='New Well', well_details=well_details, config=config)
        whp.add_well(well)
        assert len(whp.wells) == well_count + 1

    def test_exception_adding_non_well(self, manager):
        with pytest.raises(ValueError):
            manager.asset.pexes[0].wellhead_platforms[0].add_well('Not a well')


class TestWell:
    """Test parent class"""

    def test_name(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert well.name == 'NNM-3'

    def test_parent(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert isinstance(well.parent, WellHeadPlatform)

    def test_start_date(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        # assert well.start_date == datetime(2018,1,1)

    def test_active_period(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert well.active_period == 3650

    def test_choke(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert well.choke == 100

    def test_whp(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert isinstance(well.whp, WellHeadPlatform)
        assert well.whp.name == 'AEP'

    def test_pex(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert isinstance(well.pex, Pex)
        assert well.pex.name == 'Nene'

    def test_asset(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert isinstance(well.asset, Asset)
        assert well.asset.name == 'MXII'


class TestOilWell:
    """Test child class"""

    def test_defaults(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert well.ultimate_oil_recovery == 8000000
        assert well.initial_oil_rate == 5000
        assert well.gas_oil_ratio == [2000, 4000]
        assert well.b_oil == 1.0

    def test_details(self, manager):
        well = manager.asset.get_well_by_name('NNM-3')
        assert well.oil_rate == 1851
        assert well.oil_cumulative == 2846703
        assert well.gas_rate == 2072000
        assert well.gas_cumulative == 4845154174


class TestGasWell:

    def test_defaults(self, manager):
        well = manager.asset.get_well_by_name('LJM-11')
        assert well.ultimate_gas_recovery == 100000000
        assert well.initial_gas_rate == 10000000
        assert well.gas_condensate_ratio == 3.1415
        assert well.b_gas == 0.5
