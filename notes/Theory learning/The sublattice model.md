
## Temperature dependence

![img.png](figures/Gibbs energy function.png)

This equation is a polynomial fitting used to describe the temperature dependence of the Gibbs free energy of a phase.
The parameters gotten by the regression of experiment data. The physical significance of each term I asked chatGPT
directly:

            a0 represents the Gibbs free energy at absolute zero (or another reference state).
            a1T reflects the heat capacity contribution to the free energy.
            a2Tln(T) is related to the temperature dependence of the entropy.
            a4T-1 could be included to model specific temperature inversions, like electronic or magnetic contributions
            at low temperatures.
            ...

As my personal understanding, the numerical significance of this function is more important. 

Actually, the enthalpy and entropy can be obtained by this function with basic thermodynamics theory.

![img.png](figures/several state functions obtained by gibbs function.png)

Each function can be used just in limited temperature range and above the Debye temperature. (When temperature is above
Debye temperature, the Cv will be a constant and equal to 3R. Enthalpy, as the integral of heat capacity, will 
continue to increase linearly with temperature. The entropy increases linearly with the logarithm of temperature.)

The lower temperature limit is usually 298.15K, which is sufficient because the require diffusion is necessary to reach
the equilibrium.

When temperature range is large, the regression will need more T^n (n=4, 5, 6...). To decrease the number of
coefficients, several temperature ranges and expressions should be used. Usually at least two and often up to four or 
five temperature regions with different coefficients are used to describe Gibbs energy. The first order and the second 
order derivatives of each function must be continuous, otherwise it will behave like a phase transition.

The io in pycalphad accomplishes read of database and makes it ready for Gibbs energy calculation with different 
conditions. While investigating how io module works, I continued the theory learning. The follow part is theory of 
pressure dependence.

## Pressure-dependence

For condensed matters, the pressure-dependent properties are often ignored, since they are only important at very high
temperature. For condensed phases under limited pressure range, Murnaghan model is useful.

The compressibility, the inverse of bulk modulus that assumed can be expressed by a linear pressure dependence. 

![img.png](figures/compressibility.png)

K0(T) is the compressibility at 0 pressure, and n is a constant that independent with temperature and pressure. n is 
about 4 for many phases.

The expression of thermal expansivity:

![img.png](figures/thermal expansity.png)

Integrate Murnaghan model with Gibbs energy:

![img.png](figures/Murnaghen model integrate with Gibbs energy.png)

There is a new pressure-dependence model introduced, I did not describe it in details here.

## Metastable states
Gibbs energy sometimes also necessary when a compound is out of its stability temperature range. So the experimental 
data is not always enough, while this measurement may be inaccessible.

Two method: 1. extrapolations. 2. ab initio calculations.

It is necessary to estimate a value of the relative stability of the metastable structure as an “end member” of the
phase.

For extrapolations, the Kopp–Neumann rule is important.
It indicates that C$_p$(AmBn)=m×Cp(A)+n×Cp(B)

