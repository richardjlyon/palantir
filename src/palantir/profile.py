"""Classes that represent production profiles"""

import numpy as np
import pandas as pd
from palantir.facilities import OilWell
from scipy import optimize

# Initial estimate of Di for newton.optimize
OIL_WELL_INITIAL_DI = 0.000880626223092
GAS_WELL_INITIAL_DI = 0.000880626223092  # TODO check this


def _decline(di, t, qoi, b):
    return qoi / ((1 + b * di * t) ** (1 / b))


def _zero_function(di, t, qoi, b, uor):
    qo = _decline(di, t, qoi, b)
    return qo.sum() - uor


class Profiles:
    """Represents aggregated production profiles"""

    def __init__(self):
        self.curves = pd.DataFrame()

    def add(self, well):
        well_curves = Profile(well=well).curves
        self.curves = self.curves.append(well_curves)

    @property
    def field_production(self):
        return self.curves.groupby(['date'])['qo', 'qg'].sum()

    @property
    def pex_production(self):
        return self.curves.groupby(['date', 'pex'])['qo', 'qg'].sum().unstack(fill_value=0)

    @property
    def whp_production(self):
        return self.curves.groupby(['date', 'whp'])['qo', 'qg'].sum().unstack(fill_value=0)

    @property
    def well_production(self):
        return self.curves.groupby(['date', 'well'])['qo', 'qg'].sum().unstack(fill_value=0)


class Profile:
    """Represents a production profile for a Well"""

    def __init__(self, well=None):
        """Initialise a Profile"""
        self.well = well
        self._curves = None

    @property
    def curves(self):
        return self._generate_curves()

    def _generate_curves(self):

        t = pd.Series(range(0, self.well.active_period))

        if isinstance(self.well, OilWell):

            # calculate di_oil
            di_oil = optimize.newton(
                    _zero_function,
                    OIL_WELL_INITIAL_DI, args=(
                        t,
                        self.well.initial_oil_rate,
                        self.well.b_oil,
                        self.well.ultimate_oil_recovery))

            # generate oil curve
            qo = _decline(
                    di_oil,
                    t,
                    self.well.initial_oil_rate,
                    self.well.b_oil)

            # generate gas curve
            gor = self.well.gas_oil_ratio[0] + (
                    self.well.gas_oil_ratio[1] - self.well.gas_oil_ratio[0]) * t / self.well.active_period
            qg = qo * gor

            # generate condensate curve
            qc = pd.Series(np.zeros(self.well.active_period))

        else:  # it's a gas well

            # calculate di_gas
            di_gas = optimize.newton(
                    _zero_function,
                    GAS_WELL_INITIAL_DI, args=(
                        t,
                        self.well.initial_gas_rate,
                        self.well.b_gas,
                        self.well.ultimate_gas_recovery))

            # generate gas curve
            qg = _decline(
                    di_gas,
                    t,
                    self.well.initial_gas_rate,
                    self.well.b_gas)

            # generate condensate curve
            qc = qg * self.well.gas_condensate_ratio

            # generate oil curve
            qo = pd.Series(np.zeros(self.well.active_period))

        # pack into dataframe
        well_dict = {
            'asset': [self.well.asset.name.lower()] * self.well.active_period,
            'pex': [self.well.pex.name.lower()] * self.well.active_period,
            'whp': [self.well.whp.name.lower()] * self.well.active_period,
            'well': [self.well.name.lower()] * self.well.active_period,
            'date': pd.date_range(self.well.start_date, periods=self.well.active_period),
            'qo': qo,
            'qg': qg,
            'qc': qc
        }

        df = pd.DataFrame(well_dict)
        df.index = df['date']
        del df['date']
        return df
