import pandas as pd


class TestProfile:

    def test_basic(self, profile_single_existing_well):
        print("\n", profile_single_existing_well.profiles.curves)
        assert isinstance(profile_single_existing_well.profiles.curves, pd.DataFrame)

