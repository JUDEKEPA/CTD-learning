import matplotlib.pyplot as plt
from pycalphad import Database, binplot
import warnings
import os
import pytest
from symengine import Symbol
from numpy.testing import assert_allclose
import numpy as np
from pycalphad import Database, Model, calculate, equilibrium, EquilibriumError, ConditionError
from pycalphad.codegen.callables import build_callables, build_phase_records
from pycalphad.core.solver import SolverBase, Solver
from pycalphad.core.utils import get_state_variables, instantiate_models
import pycalphad.variables as v
from pycalphad.tests.fixtures import load_database, select_database



# Load database and choose the phases that will be considered
dbf = Database('/Users/zhengdiliu/SEU/LCM/CTD-learning/code/re-implement/alzn_mey.tdb') #'cfe_broshe.tdb'Al-Cu-Y.tdb
#db_test = Database()

# res = calculate(dbf, ['AL', 'ZN'], dbf.phases, T=[1400, 2500], P=101325)
                # )points={'LIQUID': [[0.1, 0.9], [0.2, 0.8], [0.3, 0.7],
                # [0.7, 0.3], [0.8, 0.2]]}
eq = equilibrium(dbf, ['AL', 'ZN'], dbf.phases,
                 {v.T: [400], v.P: 101325,
                  v.X('AL'): [0.1]}, verbose=True, to_xarray=False)


# my_phases_alzn = ['LIQUID', 'FCC_A1', 'HCP_A3']

# Create a matplotlib Figure object and get the active Axes
# fig = plt.figure(figsize=(9,6))
# axes = fig.gca()
#
# # Compute the phase diagram and plot it on the existing axes using the `plot_kwargs={'ax': axes}` keyword argument
# binplot(db_alzn, ['AL', 'Cu', 'VA'] , db_alzn.phases.keys(), {v.X('Cu'):(0,1,0.02), v.T: (300, 1800, 10), v.P:101325, v.N: 1}, plot_kwargs={'ax': axes})
# ''''''
# plt.show()
