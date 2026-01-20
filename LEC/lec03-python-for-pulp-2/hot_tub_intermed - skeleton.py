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
profit    = # YOUR CODE HERE - use zip with (350,300)
avail     = # YOUR CODE HERE - use zip with (1566,200,2880)

# Create resource dictionaries, keyed by tub names
required_dict = {}
for i in range(len(tubs)):
    # YOUR CODE HERE

# Instantiate the LP
hot_tub_lp = # YOUR CODE HERE

# Create a dict of PuLP variables (keyed by tub name)
# YOUR CODE HERE
    
# Create objective function
# YOUR CODE HERE

# Create constraints
for resource in resources:
    # YOUR CODE HERE

# The rest as before: display model, solve it, display results
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