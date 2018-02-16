from datetime import datetime

from palantir.profile import Profile
from pytest import approx


class TestOilWellProfile:

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
