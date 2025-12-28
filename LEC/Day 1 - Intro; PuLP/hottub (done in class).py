# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 08:49:03 2021

@author: IFrommer
"""

# Import the PuLP library
from pulp import *

# Create an LP model instance, store it in a Python variable
hotTubModel = LpProblem('Hot Tub LP',LpMaximize)

# Define the decision variables
x1 = LpVariable('AquaSpas',lowBound=0)
x2 = LpVariable('HydroLuxes',lowBound=0)

# Create an objective function 
hotTubModel += 350*x1 + 300*x2, 'Profit'   # label objective with string after ,

# Create the constraints
hotTubModel += x1 + x2 <= 200, 'Pumps'
hotTubModel += 9*x1 + 6*x2 <= 1566, 'Labor (hrs)'
hotTubModel += 12*x1 +16*x2 <= 2880, 'Tubing (ft)'

# Solve the LP
result = hotTubModel.solve()

# Report the results
print("Status:", LpStatus[result])

for variable in hotTubModel.variables():
    print(variable,value(variable))

print('Total profit:' , value(hotTubModel.objective))