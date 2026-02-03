# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 08:02:02 2026

@author: IFrommer
"""

from pulp import *
things = ['Shirt', 'Pants', 'Socks', 'Laptop', 'Charger', 'Snacks', 'Jacket']
lbs = [0.4, 0.8, 0.2, 2.8, 0.3, 0.7, 1.0]
lbs_dict = dict(zip(things,lbs))  # = {'Shirt': 0.4, 'Pants': 0.8, etc. }
max_pouch_wt = 3

pack_prob = LpProblem('Travel-Packing-Packing-Problem', LpMinimize)

num_things = len(things)
num_pouches = round(2 * sum(lbs) / max_pouch_wt)

pouches = range(1, num_pouches + 1)

# Decision variables
# assignment of things to pouches variable:
x = LpVariable.dicts('x', (things, pouches), cat=LpBinary)  
# pouch-used variable:
y = LpVariable.dicts('y', pouches, cat = LpBinary)   


obj = lpSum(y[j] for j in pouches), 'min number of bins'
pack_prob += obj

# constraints
for thing in things:
    thing_in_pouch = lpSum(x[thing][pouch] for pouch in pouches) == 1
    pack_prob += thing_in_pouch , f'thing {thing} goes in a pouch'

for pouch in pouches:    
    lhs = lpSum(lbs_dict[thing] * x[thing][pouch] for thing in things) 
    pack_prob += lhs <= max_pouch_wt * y[pouch], \
        f'pouch {pouch} capacity constraint'

print(pack_prob)

# Solve    
result = pack_prob.solve(PULP_CBC_CMD(msg=False))

# Display results
print('Status = ',LpStatus[result])
print('Objective value (# of pouches used): ',value(pack_prob.objective))
#  Variables
pouch_contents = dict()
for pouch in pouches:
    this_pouch_things = []
    for thing in things:
        if value(x[thing][pouch]) == 1:
            this_pouch_things.append((thing, lbs_dict[thing]))
    pouch_contents[pouch] = this_pouch_things
print('Pouch contents:\n',pouch_contents)
#print(f"Execution time: {time.perf_counter()-start_time:.4f} seconds")
#return bpp