from datetime import datetime

from palantir.facilities import Asset, OilWell, Pex, WellHeadPlatform
from palantir.profile import Profile
from pytest import approx

asset = Asset('MXII')
pex = Pex('Nene')
whp = WellHeadPlatform('WHP3')
oil_well = OilWell(name='NNM-301')

whp.add_well(oil_well)
pex.add_wellhead_platform(whp)
asset.add_pex(pex)

oil_well.active_period = 20 * 365
oil_well.start_date = datetime(2018, 1, 1)
oil_well.choke = 1.0
oil_well.ultimate_oil_recovery = 10000000
oil_well.initial_oil_rate = 5000
oil_well.gas_oil_ratio = [2000, 4000]
oil_well.b_oil = 1.0

oil_profile = Profile(oil_well)


class TestOilWellProfile:

    def test_unconstrained_oil_rate(self):
        # GIVEN an initialised, unconstrained oil well
        # WHEN the value at time zero is requested
        # THEN return the initial oil rate
        global oil_well
        global oil_profile
        assert oil_profile.curves.qo.iloc[0] == oil_well.initial_oil_rate
        assert oil_profile.curves.qg.iloc[0] == oil_well.initial_oil_rate * oil_well.gas_oil_ratio[0]
        assert oil_profile.curves.qo.iloc[365] == approx(3567, abs=1)
        assert oil_profile.curves.qg.iloc[365] == approx(7490267, abs=1)
