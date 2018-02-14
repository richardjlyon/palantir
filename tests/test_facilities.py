#!/usr/bin/env python
import pytest
from anytree import findall
from palantir.facilities import Asset, DEFAULT_CHOKE, DEFAULT_SLOTS, GasWell, OilWell, Pex, Well, WellHeadPlatform

asset = Asset('test_asset')
pex = Pex(name='test_pex')
whp = WellHeadPlatform(name='test_whp')
well = Well(name='test_well')


class TestAsset:

    def test_name(self):
        global asset
        assert asset.name == 'test_asset'

    def test_add_pex(self):
        global asset
        global pex
        asset.add_pex(pex)
        pexes = findall(asset, filter_=lambda node: type(node).__name__ == "Pex")
        assert len(pexes) > 0

    def test_exception_if_not_pex(self):
        global asset
        global pex
        with pytest.raises(ValueError):
            asset.add_pex('not a pex')

    def test_pexes(self):
        global asset
        assert len(asset.pexes) > 0


class TestPex:

    def test_name(self):
        global pex
        assert pex.name == 'test_pex'

    def test_add_wellhead_platform(self):
        global pex
        global whp
        pex.add_wellhead_platform(whp)
        whps = findall(pex, filter_=lambda node: type(node).__name__ == "WellHeadPlatform")
        assert len(whps) > 0

    def test_exception_if_not_wellhead_platform(self):
        global pex
        with pytest.raises(ValueError):
            pex.add_wellhead_platform('not a wellhead platform')

    def test_wellhead_platforms(self):
        global pex
        assert len(pex.wellhead_platforms) > 0


class TestWellHeadPlatform:

    def test_name(self):
        global whp
        assert whp.name == 'test_whp'

    def test_well_slots(self):
        global whp
        assert whp.well_slots == DEFAULT_SLOTS

    def test_add_well(self):
        global whp
        global well
        whp.add_well(well)
        wells = findall(whp, filter_=lambda node: type(node).__name__ == "Well")
        assert len(wells) > 0

    def test_exception_if_not_well(self):
        global whp
        with pytest.raises(ValueError):
            whp.add_well('not a well')

    def test_wells(self):
        global whp
        assert len(whp.wells) == 1

    def test_remaining_slots(self):
        global whp
        assert whp.remaining_slots == DEFAULT_SLOTS - 1


class TestWell:

    def test_name(self):
        global well
        assert well.name == 'test_well'

    def test_whp(self):
        global well
        assert well.whp.name == 'test_whp'

    def test_pex(self):
        global well
        assert well.pex.name == 'test_pex'

    def test_asset(self):
        global well
        assert well.asset.name == 'test_asset'

    def test_choke(self):
        global well
        assert well.choke == DEFAULT_CHOKE

    def test_exception_if_choke_not_float(self):
        global well
        with pytest.raises(ValueError):
            well.choke = 'not a Float'

    def test_exception_if_start_date_not_date(self):
        global well
        with pytest.raises(ValueError):
            well.start_date = 'not a Date()'


class TestOilWell:

    def test_name(self):
        oil_well = OilWell('test_oil_well')
        oil_well.initial_oil_rate = 5000

        assert oil_well.name == 'test_oil_well'
        assert oil_well.initial_oil_rate == 5000


class TestGasWell:

    def test_name(self):
        gas_well = GasWell('test_gas_well')
        gas_well.initial_gas_rate = 10000000

        assert gas_well.name == 'test_gas_well'
        assert gas_well.initial_gas_rate == 10000000