#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest
from palantir import make_temp_file
from palantir.manager import Manager


@pytest.fixture()
def manager():
    data = '''
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
facilities:
    asset: MXII
    pexes:
        Nene:
            AEP:
                NNM-3:
                    type: oil
                    oil rate: 1851
                    oil cumulative: 2846703
                    gas oil ratio: [2000, 4000]
                NNM-5:
                    type: oil
                    oil rate: 198
                    oil cumulative: 458645
                    gas oil ratio: [2000, 4000]
                NNM-6:
                    type: oil
                    oil rate: 1964
                    oil cumulative: 2051240
                    gas oil ratio: [2000, 4000]
            WHP4:
                NNM-401:
                    type: oil
                    oil rate: 4000
                    oil cumulative: 507833
                    gas oil ratio: [2000, 4000]
                NNM-402:
                    type: oil
                    oil rate: 1011
                    oil cumulative: 444514
                    gas oil ratio: [2000, 4000]
                NNM-403:
                    type: oil
                    oil rate: 2943
                    oil cumulative: 639181
                    gas oil ratio: [2000, 4000]
                NNM-404:
                    type: oil
                    oil rate: 3924
                    oil cumulative: 648415
                    gas oil ratio: [2000, 4000]
            WHP3:
                NNM-301:
                    type: oil
                    oil rate: 2899
                    oil cumulative: 667239
                    gas oil ratio: [2000, 4000]
                NNM-302:
                    type: oil
                    oil rate: 2943
                    oil cumulative: 433918
                    gas oil ratio: [2000, 4000]
                NNM-303:
                    type: oil
                    oil rate: 1947
                    oil cumulative: 279266
                    gas oil ratio: [2000, 4000]
                NNM-304:
                    type: oil
                    oil rate: 1556
                    oil cumulative: 108577
                    gas oil ratio: [2000, 4000]
        Litchendjili:
            LTC1:
                LJM-11:
                    type: gas
                    condensate rate: 1234
                    condensate cumulative: 987654
                    gas rate: 31415927
                    gas cumulative: 533919437
programs:
    Rig1:
        program:
            - start: 01/01/2018, WHP3
            - drill: NNM-305, oil, 70
            - drill: NNM-306, oil, 70
            - move: WHP4, 30
            - drill: NNM-405, oil, 70
            - drill: NNM-406, oil, 70
            - move: WHPL1, 30
            - drill: L14, gas, 70
            - drill: L15, gas, 70
            - standby: 100
'''
    configuration_file = make_temp_file(data)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()


data_header = """
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
facilities:
    asset: MXII
    pexes:
        Nene:
            AEP:
                NNM-3:
                    type: oil
                    oil rate: 1851
                    oil cumulative: 2846703
                    gas oil ratio: [2000, 4000]
            WHP4:
                NNM-401:
                    type: oil
                    oil rate: 4000
                    oil cumulative: 507833
                    gas oil ratio: [2000, 4000]

"""

@pytest.fixture()
def program_steps():
    data = data_header + '''
programs:
    Rig1:
        program:
            - start: 01/01/2018, AEP
            - drill: NNM-7, oil, 70
            - move: WHP4, 30
            - drill: NNM-402, gas, 70
            - standby: 100
'''
    configuration_file = make_temp_file(data)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()


@pytest.fixture()
def profile_single_existing_well():
    data = """
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
    configuration_file = make_temp_file(data)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()
