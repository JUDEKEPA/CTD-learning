
While the thermodynamics theory is profound and time-taking to learn every detail, the computational
thermodynamics narrow its range to specific application. Instead of understanding from a panoramic view, I
would like to learn from the view of how the theory becomes code.

I will try to repeat the function of pycalphad in re-implement folder. As pycalphad has been developed maturely by
talented researchers, I will basically copy the code and just implement small functions to have better understanding 
of pycalphad codes.

From what I know about computational thermodynamics right now, I list these points that I will concentrate on:

        1. The sublattice model. Before understanding how to get data (like .TDB file), I will try to understand
        what .TDB file should be like, and how to use it to calculate Gibbs energy of a certain phase with a certain
        composition.
        2. The global minimization. The step of global minimization is the key step in CALPHAD method. After learning
        how to use sublattice model to calculate Gibbs energy, it is important to understand how global minimization
        works.
        
        ....

I did not find some cases directly in .TDB file (I did not make much effort on that), but I think these theories are
also important. I made the path into two part, the theory learning will mainly base on the book while the code learning
direction will describe the code of pycalphad. When the theory learning matches the code in pycalphad, I will try to 
explain how theory becomes codes.
