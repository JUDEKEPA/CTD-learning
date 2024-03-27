from pycalphad.core.calculate import calculate
from pycalphad.io.database import Database
from pycalphad.core.utils import instantiate_models

from pycalphad.codegen.callables import build_phase_records

db_alzn = Database('cfe_broshe.tdb') #''..//cfe_broshe.tdb alzn_mey.tdb

#my_phases_alzn = ['LIQUID', 'FCC_A1', 'HCP_A3']
models = instantiate_models(db_alzn, ['Fe', 'C', 'VA'], ['BCC_A2'], model=None, parameters=dict())
# phase_records = build_phase_records(db_alzn, ['Fe', 'C', 'VA'], ['BCC_A2'], statevar_dict,
#                                             models=models, parameters=parameters,
#                                             output=output, callables=callables,
#                                             build_gradients=False, build_hessians=False,
#                                             verbose=kwargs.pop('verbose', False))
a = calculate(db_alzn, ['Fe', 'C', 'VA'], ['BCC_A2'])

#from pycalphad.core.utils import instantiate_models

#models = instantiate_models(db_alzn, ['AL', 'ZN', 'VA'], ['FCC_A1', 'HCP_A3', 'LIQUID'], model=None, parameters=dict())

