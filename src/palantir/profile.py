"""Classes that represent production profiles"""

import numpy as np
import pandas as pd
from palantir.facilities import OilWell
from scipy import optimize

# Initial estimate of Di for newton.optimize
OIL_WELL_INITIAL_DI = 0.000880626223092
GAS_WELL_INITIAL_DI = 0.000880626223092  # TODO check this


def _decline(di, t, qoi, b):
    """Arp's equation for general decline in a well
        - qoi: initial rate of production
        - di: initial decline rate
        - b: curvature (b=0 exponential)
    """
    return qoi / ((1 + b * di * t) ** (1 / b))


def _zero_function(di, t, qoi, b, uor):
    """Solve di to yield uor total barrels"""
    qo = _decline(di, t, qoi, b)
    return qo.sum() - uor


class Profiles:
    """Represents aggregated production profiles"""

    def __init__(self):
        self.curves = pd.DataFrame()

    def add(self, well):
        # well_curves = Profile(well=well).curves

        t = pd.Series(range(0, well.active_period))

        if isinstance(well, OilWell):

            di = OIL_WELL_INITIAL_DI
            b_oil = well.b_oil
            if well.is_new_well:
                initial_oil_rate = well.initial_oil_rate
                ultimate_oil_recovery = well.ultimate_oil_recovery
            else:
                initial_oil_rate = well.oil_rate
                ultimate_oil_recovery = well.ultimate_oil_recovery - well.oil_cumulative

            # calculate di_oil
            di_oil = optimize.newton(
                    _zero_function,
                    di, args=(
                        t,
                        initial_oil_rate,
                        b_oil,
                        ultimate_oil_recovery))

            # generate oil curve
            qo = _decline(
                    di_oil,
                    t,
                    initial_oil_rate,
                    b_oil)

            # generate gas curve
            gor = well.gas_oil_ratio[0] + (
                    well.gas_oil_ratio[1] - well.gas_oil_ratio[0]) * t / well.active_period
            qg = qo * gor

            # generate condensate curve
            qc = pd.Series(np.zeros(well.active_period))

        else:  # it's a gas well

            # calculate di_gas
            di_gas = optimize.newton(
                    _zero_function,
                    GAS_WELL_INITIAL_DI, args=(
                        t,
                        well.initial_gas_rate,
                        well.b_gas,
                        well.ultimate_gas_recovery))

            # generate gas curve
            qg = _decline(
                    di_gas,
                    t,
                    well.initial_gas_rate,
                    well.b_gas)

            # generate condensate curve
            qc = qg * well.gas_condensate_ratio

            # generate oil curve
            qo = pd.Series(np.zeros(well.active_period))

        # pack into dataframe
        well_dict = {
            'asset': [well.asset.name.lower()] * well.active_period,
            'pex': [well.pex.name.lower()] * well.active_period,
            'whp': [well.whp.name.lower()] * well.active_period,
            'well': [well.name.lower()] * well.active_period,
            'date': pd.date_range(well.start_date, periods=well.active_period),
            'qo': qo,
            'qg': qg,
            'qc': qc
        }

        df = pd.DataFrame(well_dict)
        df.index = df['date']
        del df['date']

        self.curves = self.curves.append(df)

    @property
    def field_production(self):
        return self.curves.groupby(['date'])['qo', 'qg', 'qc'].sum()

    @property
    def pex_production(self):
        return self.curves.groupby(['date', 'pex'])['qo', 'qg', 'qc'].sum().unstack(fill_value=0)

    @property
    def whp_production(self):
        return self.curves.groupby(['date', 'whp'])['qo', 'qg', 'qc'].sum().unstack(fill_value=0)

    @property
    def well_production(self):
        return self.curves.groupby(['date', 'well'])['qo', 'qg', 'qc'].sum().unstack(fill_value=0)
