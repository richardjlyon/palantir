""" Classes that represent physical facilities"""

from datetime import datetime

from anytree import NodeMixin, findall

DEFAULT_SLOTS = 6  # TODO Fix
DEFAULT_CHOKE = 1


class Asset(NodeMixin):
    """Represents the Asset. Root of a tree that represents the facilities in the Asset."""

    def __init__(self, name=None):
        self.name = name

    def add_pex(self, pex):
        if isinstance(pex, Pex):
            pex.parent = self
            return self
        else:
            raise ValueError("Can't add {} to Asset".format(type(pex)))

    @property
    def pexes(self):
        return findall(self, filter_=lambda node: type(node).__name__ == "Pex")


class Pex(NodeMixin):
    """Represents a Pex in an Asset"""

    def __init__(self, name=None):
        self.parent = None
        self.name = name

    def add_wellhead_platform(self, wellhead_platform):
        if isinstance(wellhead_platform, WellHeadPlatform):
            wellhead_platform.parent = self
            return self
        else:
            raise ValueError("Can't add {} to Pex".format(type(wellhead_platform)))

    @property
    def wellhead_platforms(self):
        return findall(self, filter_=lambda node: type(node).__name__ == "WellHeadPlatform")


class WellHeadPlatform(NodeMixin):
    """Represents a Wellhead Platform in an Asset"""

    def __init__(self, name=None, well_slots=DEFAULT_SLOTS):
        self.parent = None
        self.name = name
        self.well_slots = well_slots

    def add_well(self, well):
        if isinstance(well, Well):
            well.parent = self
            return self
        else:
            raise ValueError("Can't add {} to Wellhead Platform".format(type(well)))

    @property
    def wells(self):
        return findall(self, filter_=lambda node: type(node).__name__ == "Well")

    @property
    def remaining_slots(self):
        return self.well_slots - len(self.wells)


class Well(NodeMixin):
    """Represents a Well in an Asset"""

    def __init__(self, name=None):
        self.parent = None
        self.name = name
        self._choke = DEFAULT_CHOKE
        self._start_date = None
        self.active_period = None

    @property
    def choke(self):
        return self._choke

    @choke.setter
    def choke(self, value):
        if isinstance(value, float):
            self._choke = value
        else:
            raise ValueError("Couldn't set choke with type {}".format(type(value)))

    @property
    def whp(self):
        return self.parent

    @property
    def pex(self):
        return self.whp.parent

    @property
    def asset(self):
        return self.pex.parent

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if isinstance(value, datetime):
            self._start_date = value
        else:
            raise ValueError("Couldn't set start_date with type {}".format(type(value)))


class OilWell(Well):
    """Represents an oil well in an Asset"""

    def __init__(self, name=None):
        super().__init__(name=name)
        self.ultimate_oil_recovery = None
        self.initial_oil_rate = None
        self.gas_oil_ratio = None
        self.b_oil = None


class GasWell(Well):
    """Represents a gas well in an Asset"""

    def __init__(self, name=None):
        super().__init__(name=name)
        self.ultimate_gas_recovery = None
        self.initial_gas_rate = None
        self.gas_condensate_ratio = None
        self.b_gas = None
