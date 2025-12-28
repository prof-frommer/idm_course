# -*- coding: utf-8 -*-
"""
hotTubBasicFilledIn.py - Created on Tue Jan  8 13:03:05 2019
Basic version of Hot Tub in PuLP 
@author: ifrommer
"""

# Import the PuLP library
from pulp import *

# Create an LP model instance, store it in a Python variable
hotTubModel = LpProblem('Hot Tub LP',LpMaximize)

# Create the LP variables
x1 = LpVariable('AquaSpas',lowBound=0)    # default category is continuous
x2 = LpVariable('HydroLuxes',lowBound=0)

# Create objective function
hotTubModel += 350*x1 + 300*x2, 'Profit'

# Create constraints
hotTubModel += x1 + x2 <= 200, 'Pumps'
hotTubModel += 9*x1 + 6*x2 <= 1566, 'Labor (hrs)'
hotTubModel += 12*x1 + 16*x2 <= 2880, 'Tubing (ft)'

# Print formulated model and optionally write it to a file
print(hotTubModel)
hotTubModel.writeLP('hotTubModelLP.txt')

# Solve
result = hotTubModel.solve()

# Print results
print("Status: ",LpStatus[result])
for variable in hotTubModel.variables():
        print(str(variable).ljust(12),' = ',value(variable))
print("Total Profit = %8.2f" % value(hotTubModel.objective))