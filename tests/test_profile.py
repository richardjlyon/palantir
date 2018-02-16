from datetime import datetime

import pytest
from palantir import make_temp_file
from palantir.manager import Manager
from palantir.profile import Profile
from pytest import approx

simple = '''
defaults:
    well:
        choke: 100
        active period: 7300 # days
        oil well:
            ultimate oil recovery: 10000000
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
            WHP3:
                NNM-301:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 667239
                    gas rate: 6899247
                    gas cumulative: 1479210651
drilling:
    Rig1:
        program:
            - start: 01/01/2018, WHP3

    '''


@pytest.fixture()
def manager():
    global simple
    configuration_file = make_temp_file(simple)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()


class TestOilWEllProfile2:

    def test_unconstrained__oil_rate(self, manager):
        # GIVEN an initialised, unconstrained oil well
        # WHEN the value at time zero is requested
        # THEN return the initial oil rate
        nnm301 = manager.asset.pexes[0].wellhead_platforms[0].wells[0]
        nnm301.start_date = datetime(2018, 1, 1)
        oil_profile = Profile(nnm301)
        assert oil_profile.curves.qo.iloc[0] == nnm301.initial_oil_rate
        assert oil_profile.curves.qg.iloc[0] == nnm301.initial_oil_rate * nnm301.gas_oil_ratio[0]
        assert oil_profile.curves.qo.iloc[365] == approx(3567, abs=1)
        assert oil_profile.curves.qg.iloc[365] == approx(7490267, abs=1)
