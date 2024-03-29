import matplotlib.pyplot as plt
from pycalphad import Database, binplot
import pycalphad.variables as v

# Load database and choose the phases that will be considered
db_alzn = Database('Al-Cu-Y.tdb') #'cfe_broshe.tdb'Al-Cu-Y.tdbalzn_mey.tdb
db_test = Database()


# my_phases_alzn = ['LIQUID', 'FCC_A1', 'HCP_A3']

# Create a matplotlib Figure object and get the active Axes
fig = plt.figure(figsize=(9,6))
axes = fig.gca()

# Compute the phase diagram and plot it on the existing axes using the `plot_kwargs={'ax': axes}` keyword argument
binplot(db_alzn, ['AL', 'Cu', 'VA'] , db_alzn.phases.keys(), {v.X('Cu'):(0,1,0.02), v.T: (300, 1800, 10), v.P:101325, v.N: 1}, plot_kwargs={'ax': axes})
''''''
plt.show()
