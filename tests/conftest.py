#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pytest
from palantir import make_temp_file
from palantir.manager import Manager


@pytest.fixture()
def manager_simple_configuration():
    data = '''
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
programs:
    Rig1:
        program:
            - start: 01/01/2018, WHP3

    '''
    configuration_file = make_temp_file(data)
    m = Manager(configuration_file.name)
    yield m
    configuration_file.close()
