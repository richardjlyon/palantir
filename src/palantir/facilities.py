""" Classes that represent physical facilities"""

from datetime import datetime

from anytree import NodeMixin, findall

DEFAULT_SLOTS = 6  # TODO Fix
DEFAULT_CHOKE = 1


class Asset(NodeMixin):
    """Represents the Asset. Root of a tree that represents the facilities in the Asset."""

    def __init__(self, name=None, defaults=None):
        self.name = name
        self.defaults = defaults

    def add_pex(self, pex):
        if isinstance(pex, Pex):
            pex.parent = self
            return self
        else:
            raise ValueError("Can't add {} to Asset".format(type(pex)))

    @property
    def pexes(self):
        return findall(self, filter_=lambda node: type(node).__name__ == "Pex")

    def __repr__(self):
        return "Asset:{}".format(self.name)


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

    def __repr__(self):
        return "Pex:{}".format(self.name)


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
        oil_wells = findall(self, filter_=lambda node: type(node).__name__ == "OilWell")
        gas_wells = findall(self, filter_=lambda node: type(node).__name__ == "GasWell")
        return oil_wells + gas_wells

    @property
    def remaining_slots(self):
        return self.well_slots - len(self.wells)

    def __repr__(self):
        return "WellHeadPlatform:{}".format(self.name)


class Well(NodeMixin):
    """Represents a Well in an Asset"""

    # {'type': 'oil', 'oil rate': 1964, 'oil cumulative': 2051240, 'gas rate': 8963974, 'gas cumulative': 7378218973}

    def __init__(self, name=None, well_details=None, defaults=None):
        self.parent = None
        self.name = name
        if defaults:
            self.active_period = defaults['active period']
            self.choke = defaults['choke']
        else:
            self.active_period = 0
            self.choke = 0
        self._details = well_details
        self._start_date = None

    @property
    def choke(self):
        return self._choke

    @choke.setter
    def choke(self, value):
        if isinstance(value, int):
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

    def __repr__(self):
        return "Well:{}".format(self.name)


class OilWell(Well):
    """Represents an oil well in an Asset"""

    def __init__(self, name=None, well_details=None, defaults=None):
        super().__init__(name=name, well_details=well_details, defaults=defaults)
        # defaults
        self.ultimate_oil_recovery = defaults['ultimate oil recovery']
        self.initial_oil_rate = defaults['initial oil rate']
        self.gas_oil_ratio = defaults['gas oil ratio']
        self.b_oil = defaults['b oil']
        # details
        self.oil_rate = well_details['oil rate']
        self.oil_cumulative = well_details['oil cumulative']
        self.gas_rate = well_details['gas rate']
        self.gas_cumulative = well_details['gas cumulative']


class GasWell(Well):
    """Represents a gas well in an Asset"""

    def __init__(self, name=None, well_details=None, defaults=None):
        super().__init__(name=name, well_details=well_details, defaults=defaults)
        # defaults
        self.ultimate_gas_recovery = defaults['ultimate gas recovery']
        self.initial_gas_rate = defaults['initial gas rate']
        self.gas_condensate_ratio = defaults['gas condensate ratio']
        self.b_gas = defaults['b gas']
        # details
        self.condensate_rate = well_details['condensate rate']
        self.condensate_cumulative = well_details['condensate cumulative']
        self.gas_rate = well_details['gas rate']
        self.gas_cumulative = well_details['gas cumulative']
