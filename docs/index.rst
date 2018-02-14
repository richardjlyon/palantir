========
palantir
========

This is the documentation of **palantir**.

.. note::

Forecaster predicts the oil and gas that will be produced by a system of wells, and the cost of producing it.
Wells may already exist, or be created.

Wells  produce some combination of oil, gas, and condensate, which varies over time.
There are two types of well - oil wells, and gas wells.

A well becomes active after it has been drilled. At any time in its active period, it has a maximum rate, above which it can't produce. The rate starts at an initial value and declines over time. The well is assumed to be inactive after its potential falls below a defined rate. The duration of the active period, and the volume produced during the active period, are defined. It has a decline rate that causes that volume to be produced in the active period.
During the active period, production may be reduced below the well's potential. Choking a well increases the length of its active period.
Oil wells produce gas at  rate defined by a gas/oil ratio. Gas/oil ratio varies over time.

Gas wells produce condensate at a rate defined by a gas/condensate ratio. Gas/condensate ratio varies over time.
Wells are created by rigs, on well head platforms, in licence areas.

Well head platforms have a defined number of slots, which can vary. A platform takes a defined amount of time and money to create. Money is spent at a fixed rate during the creation time.
A rig can drill one well at a time on a well head platform. A rig requires a defined amount of time to drill a well, which can vary over time. A rig costs a defined amount of money while drilling. A rig can move between well head platforms and requires a defined amount of time and money to do so. A rig can standby for defined amounts of time and requires a defined amount of money to do so.
The activity of the rig is defined by a program. A program is a sequence of steps executied in order. A step is an action and a set of parameters.

Production is the aggregate of the oil, gas, and condensate production from the active wells. Production is availble for individual wells, and aggregated for licences and well head platforms.
Total production may be constrained by oil, gas, or condensate limits. Limits may be imposed at well, well head platform, or system level, and vary over time.


Contents
========

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
