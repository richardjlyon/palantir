""" Classes that represent physical facilities"""

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

    @property
    def wellhead_platforms(self):
        return findall(self, filter_=lambda node: type(node).__name__ == "WellHeadPlatform")

    @property
    def wells(self):
        oil_wells = findall(self, filter_=lambda node: type(node).__name__ == "OilWell")
        gas_wells = findall(self, filter_=lambda node: type(node).__name__ == "GasWell")
        return oil_wells + gas_wells

    def get_wellhead_platform_by_name(self, wellhead_platform_name):
        return next((wellhead_platform for wellhead_platform in self.wellhead_platforms if
                     wellhead_platform.name == wellhead_platform_name), None)

    def get_well_by_name(self, well_name):
        return next((well for well in self.wells if well.name == well_name), None)

    def __str__(self):
        return "Asset:{}".format(self.name)


class Pex(NodeMixin):
    """Represents a Pex in an Asset"""

    def __init__(self, name=None):
        self.parent = None
        self.name = name

    @property
    def wellhead_platforms(self):
        return findall(self, filter_=lambda node: type(node).__name__ == "WellHeadPlatform")

    def add_wellhead_platform(self, wellhead_platform):
        if isinstance(wellhead_platform, WellHeadPlatform):
            wellhead_platform.parent = self
            return self
        else:
            raise ValueError("Can't add {} to Pex".format(type(wellhead_platform)))

    def __repr__(self):
        return "Pex:{}".format(self.name)


class WellHeadPlatform(NodeMixin):
    """Represents a Wellhead Platform in an Asset"""

    def __init__(self, name=None, well_slots=DEFAULT_SLOTS):
        self.parent = None
        self.name = name
        self.well_slots = well_slots

    @property
    def wells(self):
        oil_wells = findall(self, filter_=lambda node: type(node).__name__ == "OilWell")
        gas_wells = findall(self, filter_=lambda node: type(node).__name__ == "GasWell")
        return oil_wells + gas_wells

    @property
    def remaining_slots(self):
        return self.well_slots - len(self.wells)

    def add_well(self, well):
        if isinstance(well, Well):
            well.parent = self
            return self
        else:
            raise ValueError("Can't add {} to Wellhead Platform".format(type(well)))
        return oil_wells + gas_wells

    def __repr__(self):
        return "WellHeadPlatform:{}".format(self.name)


class Well(NodeMixin):
    """Represents a Well in an Asset"""

    def __init__(self, name=None, start_date=None, well_details=None, well_defaults=None):

        self.parent = None
        self.name = name
        self.active_period = well_defaults['active period']
        self.choke = well_defaults['choke']

        if well_details:
            self.is_new_well = False
            self.start_date = well_defaults['start date']
        else:
            self.is_new_well = True
            self.start_date = start_date

    @property
    def whp(self):
        return self.parent

    @property
    def pex(self):
        return self.whp.parent

    @property
    def asset(self):
        return self.pex.parent

    def __repr__(self):
        return "Well:{}".format(self.name)


# TODO move gas to Well

class OilWell(Well):
    """Represents an oil well in an Asset"""

    def __init__(self, name=None, start_date=None, well_details=None, well_defaults=None):
        super().__init__(name=name, start_date=start_date, well_details=well_details, well_defaults=well_defaults)
        # defaults
        self.ultimate_oil_recovery = well_defaults['ultimate oil recovery']
        self.initial_oil_rate = well_defaults['initial oil rate']
        self.gas_oil_ratio = well_defaults['gas oil ratio']
        self.b_oil = well_defaults['b oil']
        # details
        if well_details:
            # It's an existing well
            self.oil_rate = well_details['oil rate']
            self.oil_cumulative = well_details['oil cumulative']
            self.gas_oil_ratio = well_details['gas oil ratio']


class GasWell(Well):
    """Represents a gas well in an Asset"""

    def __init__(self, name=None, start_date=None, well_details=None, well_defaults=None):
        super().__init__(name=name, start_date=start_date, well_details=well_details, well_defaults=well_defaults)
        # defaults
        self.ultimate_gas_recovery = well_defaults['ultimate gas recovery']
        self.initial_gas_rate = well_defaults['initial gas rate']
        self.gas_condensate_ratio = well_defaults['gas condensate ratio']
        self.b_gas = well_defaults['b gas']
        # details
        if well_details:
            self.condensate_rate = well_details['condensate rate']
            self.condensate_cumulative = well_details['condensate cumulative']
            self.gas_rate = well_details['gas rate']
            self.gas_cumulative = well_details['gas cumulative']
