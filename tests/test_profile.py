from datetime import datetime

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

    def test_basic(self, profile_single_existing_well):
        assert isinstance(profile_single_existing_well.profiles.curves, pd.DataFrame)


class TestSingleExistingOilWell:
    """Ensure an oil well generates the correct oil ang gas profiles"""

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

    def test_new_oil_well_at_time_zero(self):
        # GIVEN a single, new oil well at time 0
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

    def test_new_oil_well_deferred(self):
        # GIVEN a single, new oil well at time 0
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
            - standby: 30
            - drill: NNM-305, oil, 70     
"""
        curves = generate_manager(well_data).profiles.curves
        assert curves.index[0] == datetime(2018, 1, 31)
        assert curves.qo.iloc[0] == 5000


class TestSingleExistingGasWell:
    """Ensure a gas well generates the correct profiles"""

    @pytest.mark.skip(reason="Haven't figured out how to handle gas well decline")
    def test_existing_gas_well(self):
        # GIVEN a single, existing gas well
        # WHEN getting oil, gas and condensate values at time zero and time 365
        # THEN it returns the correct values
        pass


class TestAggregationOfProfiles:
    """Ensure profile aqgregation works correctly for wells, wellhead plaforms, pexes, and asset"""

    def test_combining_two_existing_oil_wells(self):
        # GIVEN two existing oil well
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
                NNM-5:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]  
        """

        profiles = generate_manager(well_data).profiles
        nnm3_o = profiles.well_production.qo['nnm-3']
        nnm5_o = profiles.well_production.qo['nnm-5']
        nnm3_g = profiles.well_production.qg['nnm-3']
        nnm5_g = profiles.well_production.qg['nnm-5']
        nnm3_c = profiles.well_production.qc['nnm-3']
        nnm5_c = profiles.well_production.qc['nnm-5']

        total_o = nnm3_o + nnm5_o
        assert total_o.iloc[0] == 10000
        assert total_o.iloc[365] == approx(7485, abs=1)

        total_g = nnm3_g + nnm5_g
        assert total_g.iloc[0] == 20000000
        assert total_g.iloc[365] == approx(16467360, abs=1)

        total_c = nnm3_c + nnm5_c
        assert total_c.iloc[0] == 0
        assert total_c.iloc[365] == 0

    def test_whp_production(self):
        # GIVEN two existing oil well
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
                NNM-5:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000] 
            WHP3:
                NNM-301:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]   
        """

        profiles = generate_manager(well_data).profiles
        aep_o = profiles.whp_production.qo['aep']
        whp3_o = profiles.whp_production.qo['whp3']

        total_o = aep_o + whp3_o
        assert aep_o.iloc[0] == 10000
        assert whp3_o.iloc[0] == 5000
        assert total_o.iloc[0] == 15000
        assert total_o.iloc[365] == approx(11228, abs=1)

    def test_pex_production(self):
        # GIVEN two existing oil well
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
                NNM-5:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000] 
            WHP3:
                NNM-301:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]
        Litchendjili:
            LTCH1:
                LTCH-1:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]  
        """

        profiles = generate_manager(well_data).profiles
        nene_o = profiles.pex_production.qo['nene']
        ltch_o = profiles.pex_production.qo['litchendjili']

        total_o = nene_o + ltch_o
        assert nene_o.iloc[0] == 15000
        assert ltch_o.iloc[0] == 5000
        assert total_o.iloc[0] == 20000
        assert total_o.iloc[365] == approx(14970, abs=1)

    def test_field_production(self):
        # GIVEN two existing oil well
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
                NNM-5:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000] 
            WHP3:
                NNM-301:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]
        Litchendjili:
            LTCH1:
                LTCH-1:
                    type: oil
                    oil rate: 5000
                    oil cumulative: 0
                    gas oil ratio: [2000, 4000]  
        """

        profiles = generate_manager(well_data).profiles
        mxii_o = profiles.field_production.qo
        assert mxii_o.iloc[0] == 20000
        assert mxii_o.iloc[365] == approx(14970, abs=1)
