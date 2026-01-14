# -*- coding: utf-8 -*-
"""
hot_tub_basic.py - Jan  8 2013+
Basic version of Hot Tub in PuLP (assumes >= versn 2.70 w/ GLPK solver)
@author: ifrommer
"""

# Import the PuLP library
from pulp import *

# Create an LP model instance, store it in a Python variable
hot_tub_lp = LpProblem('Hot Tub LP',LpMaximize)

# Create the LP variables
x1 = LpVariable('AquaSpas',lowBound=0)    # default category is continuous
x2 = LpVariable('HydroLuxes',lowBound=0)

# Create objective function
hot_tub_lp += 350*x1 + 300*x2, 'Profit'

# Create constraints
hot_tub_lp += x1 + x2 <= 200, 'Pumps'
hot_tub_lp += 9*x1 + 6*x2 <= 1566, 'Labor (hrs)'
hot_tub_lp += 12*x1 + 16*x2 <= 2880, 'Tubing (ft)'

# Print formulated model and optionally write it to a file
print(hot_tub_lp)
hot_tub_lp.writeLP('hot_tub_lp.txt')

# Solve (argument to suppress GLPK output)
result = hot_tub_lp.solve(GLPK(msg=False))

# Print solver status and optimal variable values
print("Status: ",LpStatus[result])
for variable in hot_tub_lp.variables():
        print(f'{str(variable):<12} = {value(variable)}')
#  Print objective value
obj_value = value(hot_tub_lp.objective)
print(f'Total Profit = {obj_value:8.2f}')
