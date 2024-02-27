import numpy as np
import matplotlib.pyplot as plt
import math

AC_BD_end_member_G = -10000
AD_BC_end_member_G = -5000

def srf_Gm(fraction_A, fraction_C):
    return AC_BD_end_member_G * fraction_A * fraction_C + \
        AD_BC_end_member_G * fraction_A * (1-fraction_C) + \
        AD_BC_end_member_G * (1-fraction_A) * fraction_C + \
        AC_BD_end_member_G * (1-fraction_A) * (1-fraction_C)


print(srf_Gm(0.1, 0.2))


def cnf_Sm(fraction_A, fraction_C):
    return -8.314 * (0.5 * (fraction_A * math.log(fraction_A, math.e)+(1-fraction_A) * math.log((1-fraction_A), math.e)) + \
                     0.5 * (fraction_C * math.log(fraction_C, math.e)+(1-fraction_C) * math.log((1-fraction_C), math.e)))


print(cnf_Sm(0.5, 0.5))

T = 400

def G_m_theta(fraction_A, fraction_C):
    return srf_Gm(fraction_A, fraction_C) - T * cnf_Sm(fraction_A, fraction_C)

def hillert_excess_energy(fraction_A, fraction_C):
    return (fraction_A*fraction_C*(1-fraction_A)*(1-fraction_C))**0.5 * (-10000**2/12/8.314/400)

def G_m_theta_hillert(fraction_A, fraction_C):
    return srf_Gm(fraction_A, fraction_C) - T * cnf_Sm(fraction_A, fraction_C) + hillert_excess_energy(fraction_A, fraction_C)


print(G_m_theta(0.5, 0.5))

A = 0.01
C = 0.01

constituent_square = []




while A <= 0.9901:
    C = 0.01
    while C <= 0.9901:
        constituent_square.append([A, C])
        C += 0.001
    A += 0.001

result = []
# Hillert suggested the use of a special reciprocal parameter
Hillert_result = []


for i in constituent_square:
    result.append(G_m_theta(i[0], i[1]))
    Hillert_result.append(G_m_theta_hillert(i[0], i[1]))





''''''
xx = [i[0] for i in constituent_square]
yy = [i[1] for i in constituent_square]


plt.figure(figsize=(8, 6))
plt.scatter(xx, yy, c=Hillert_result)
plt.colorbar(label='Value')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Color corresponds to the value in the x-y plane')
plt.show()




