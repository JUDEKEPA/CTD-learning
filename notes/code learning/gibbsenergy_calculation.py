from pycalphad.core.calculate import calculate
from pycalphad.io.database import Database

db_alzn = Database('alzn_mey.tdb') #''..//cfe_broshe.tdb

my_phases_alzn = ['LIQUID', 'FCC_A1', 'HCP_A3']

a = calculate(db_alzn, ['AL', 'ZN', 'VA'], ['FCC_A1', 'HCP_A3', 'LIQUID'])