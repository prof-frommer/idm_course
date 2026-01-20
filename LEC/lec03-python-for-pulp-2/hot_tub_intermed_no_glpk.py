"""
Intermediate Hot tub        updated 2025_01_17
with: dicts, lpSum        without: AMPLY
"""
# Import the pulp library
from pulp import *

# Define problem data
tubs      = ['Aqua','Hydro']
resources = ['Labor','Pumps','Tubing']
required  = ((9,1,12),(6,1,16))
profit    = dict(zip(tubs,(350,300)))
avail     = dict(zip(resources,(1566,200,2880)))

# Create resource dictionaries, keyed by tub names
required_dict = {}
for i in range(len(tubs)):
    required_dict[tubs[i]] = dict(zip(resources,required[i]))
# diagnostic
#print(required_dict)

# Instantiate the LP
hot_tub_lp = LpProblem('HotTubLP',sense=LpMaximize)

# Create a dict of PuLP variables (keyed by tub name)
x = LpVariable.dicts('x', tubs, lowBound=0)
# diagnostics
"""print('Variable values:')
for var in x.values():
    print(var,value(var))"""
    
# Create objective function
hot_tub_lp += lpSum(profit[i]*x[i] for i in tubs), 'Total Profit'
# diagnostics
"""print('Objective:  ',hot_tub_lp.objective,value(hot_tub_lp.objective))
x['Aqua'].varValue = 2; x['Hydro'].varValue = 1
print('Setting variable values to 2 and 1')
print('Objective:  ',hot_tub_lp.objective,value(hot_tub_lp.objective))"""

# Create constraints
for resource in resources:
    constr_LHS = lpSum(required_dict[tub][resource]*x[tub] for tub in tubs)
    hot_tub_lp += constr_LHS <= avail[resource], resource

# The rest as before: display model, solve it, display results
# Print formulated model and optionally write it to a file
print(hot_tub_lp)
hot_tub_lp.writeLP('hot_tub_lp.txt')

result = hot_tub_lp.solve()

# Print solver status and optimal variable values
print("Status: ",LpStatus[result])
for variable in hot_tub_lp.variables():
        print(f'{str(variable):<12} = {value(variable)}')
#  Print objective value
obj_value = value(hot_tub_lp.objective)
print(f'Total Profit = {obj_value:8.2f}')