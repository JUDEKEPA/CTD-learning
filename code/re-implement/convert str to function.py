import numpy as np
from sympy import symbols, lambdify, sympify
import matplotlib
matplotlib.use('agg')  # Use 'agg' backend
import matplotlib.pyplot as plt


# Define the temperature symbol
T = symbols('T')

# Example equation string
equation_str = "-7976.15 + 137.0715*T - 24.36720*T*log(T) - 1.884662E-3*T**2 - 0.877664E-6*T**3 + 74092*T**(-1)"

# Convert the string to a sympy expression
equation_expr = sympify(equation_str)

# Convert the sympy expression to a function using numpy
equation_func = lambdify(T, equation_expr, modules=['numpy'])

# Now you can use equation_func as a regular Python function
temperature = 300  # Example temperature in Kelvin
result = equation_func(temperature)
print(result)

x = np.linspace(298.15, 2298.15, 1000)
y = equation_func(x)

plt.figure()
plt.plot(x, y)
plt.show()


