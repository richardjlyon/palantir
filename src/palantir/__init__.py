# -*- coding: utf-8 -*-
from tempfile import NamedTemporaryFile

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


def make_temp_file(content):
    '''helper function to make small config files for testing'''
    with NamedTemporaryFile('r+', delete=False) as temp:
        temp.write(content)
        return temp


def debug(string):
    return "\n>>> {}".format(string)
