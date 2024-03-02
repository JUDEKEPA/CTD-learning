## Introduction

When I learn the book 'Computational Thermodynamics: The Calphad Method', I found there is no detailed explanation of
the global minimization algorithm. I want to learn how this achieved by reading the code of pycalphad.

### io module

The function of io module is to convert the .tdb file to equations and conditions executable by codes. I'd like to skip
this part.

### calculation part

I am curious how pycalphad done the calculations while it is really complex to me, I want to start part by part. I think
I can begin with calculate.py file or equilibrium file.

#### Building of model and phase_records


    if phase_records is None:
        models = instantiate_models(dbf, comps, active_phases, model=model, parameters=parameters)
        phase_records = build_phase_records(dbf, comps, active_phases, statevar_dict,
                                            models=models, parameters=parameters,
                                            output=output, callables=callables,
                                            build_gradients=False, build_hessians=False,
                                            verbose=kwargs.pop('verbose', False))

