# -*- coding: utf-8 -*-
"""  hot_tub_amply.py
- uses dictionaries and AMPLY (AMPLY is outside of PuLP as of v2.70)
- last updated 1/8/23
"""
# Import pulp and amply
from pulp import *
from amply import *

# Define some file names for use
DAT_FILE = 'blue.dat'
LP_FILE = 'hot_tub_lp.txt'    # stores formulated model

# Set up the AMPLY data structure
data = Amply("""
             set products;
             set resources;
             param profit{products};
             param avail{resources};
             param req{resources, products};
             """)

# Load the AMPLY data stored in the file DAT_FILE
data.load_file(open(DAT_FILE))

# Create the 'hot_tub_lp' variable to contain the problem data
hot_tub_lp = LpProblem("The_Hot_Tub_Problem",LpMaximize)

# Create a dictionary of PuLP variables with keys being the various hot tubs
x = LpVariable.dicts('x',data.products, lowBound=0)

# Add objective
hot_tub_lp += lpSum(data.profit[tub] * x[tub] for tub in data.products), \
    "Total Profit"

# loop to add each resource constraint
for resource in data.resources:
    lhs = lpSum(data.req[resource][tub] * x[tub] for tub in data.products)
    hot_tub_lp += lhs <= data.avail[resource], resource

# Print model to console and to a textfile
print(hot_tub_lp)    
hot_tub_lp.writeLP(LP_FILE)

# Solve the LP  (argument suppresses output)
result = hot_tub_lp.solve(PULP_CBC_CMD(msg=False))
""" results in LpStatus = {0:'Not Solved', 1:'Optimal', 
 -1: 'Infeasible', -2: 'Unbounded', -3: 'Undefined'}"""
             
# Print solver status and optimal variable values
print("Status: ",LpStatus[result])
for variable in hot_tub_lp.variables():
    print(f'{str(variable):<12} = {value(variable)}')
#  Print objective value
obj_value = value(hot_tub_lp.objective)
print(f'Total Profit = {obj_value:8.2f}')