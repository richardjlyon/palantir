import pandas as pd


class TestProfile:

    def test_basic(self, profile_single_existing_well):
        assert isinstance(profile_single_existing_well.profiles, pd.DataFrame)
