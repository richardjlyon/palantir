import pandas as pd
import pytest
from palantir.manager import Manager
from pytest import approx


def generate_manager(data):
    header = '''
description:
    start date: 01/01/2018
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
            ultimate gas recovery: 100000000
            initial gas rate: 10000000
            gas condensate ratio: 3.1415
            b gas: 0.5
'''

    file_path = '/Users/richardlyon/temp_file.yaml'

    with open(file_path, 'w') as file:
        file.write(header + data)

    return Manager(file_path)


class TestProfile:

    @pytest.mark.skip
    def _test_basic(self, profile_single_existing_well):
        assert isinstance(profile_single_existing_well.profiles.curves, pd.DataFrame)


class TestSingleExistingOilWell:
    """Ensure an oil well genertes the correct oil ang gas profiles"""

    def test_existing_oil_well(self):
        # GIVEN a single, existing oil well
        # WHEN getting oil, gas and condensate values at time zero and time 365
        # THEN it returns the correct values
        well_data = """
facilities:
    asset: MXII
    pexes:
        Nene:
            AEP:
                NNM-3:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]        
        """

        curves = generate_manager(well_data).profiles.curves

        assert curves.qo.iloc[0] == 5000
        assert curves.qg.iloc[0] == 10000000
        assert curves.qc.iloc[0] == 0
        assert curves.qo.iloc[365] == approx(3742, abs=1)
        assert curves.qg.iloc[365] == approx(8233680, abs=1)
        assert curves.qc.iloc[365] == 0

    @pytest.mark.skip(reason="Haven't figured out how to handle gas well decline")
    def test_existing_gas_well(self):
        # GIVEN a single, existing gas well
        # WHEN getting oil, gas and condensate values at time zero and time 365
        # THEN it returns the correct values
        pass

    def test_new_oil_well_at_time_zero(self):
        # GIVEN a single, existing oil well at time 0
        # WHEN getting oil, gas and condensate values at time zero and time 365
        # THEN it returns the correct values
        well_data = """
facilities:
    asset: MXII
    pexes:
        Nene:
            WHP3:
programs:
    Rig1:
        program:
            - start: 01/01/2018, WHP3
            - drill: NNM-305, oil, 70     
"""
        curves = generate_manager(well_data).profiles.curves
        assert curves.qo.iloc[0] == 5000
        assert curves.qg.iloc[0] == 10000000
        assert curves.qc.iloc[0] == 0
        assert curves.qo.iloc[365] == approx(3742, abs=1)
        assert curves.qg.iloc[365] == approx(8233680, abs=1)
        assert curves.qc.iloc[365] == 0
