# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:18:25 2019

@author: ifrommer
"""

from pulp import *
from amply import *

def diet_lp(dat_file_name):
    diet_lp_model = LpProblem(name='Diet LP',sense=LpMinimize)
    
    # Names within must match names in .dat file
    data = Amply("""
    set food_items;
    set nutrients;
    param objective{food_items};
    param reqs{nutrients};
    param supply{food_items,nutrients};
    param max_for_item{food_items};
    """)
    
    # dat_file_name = 'wardRoom1.dat'
    data.load_file(open(dat_file_name))
    
    # diagnostic to see if things loaded and get used to indexing
    for nutr in data.nutrients:
       print('required ',nutr,data.reqs[nutr]) 
       for food in data.food_items:
           print('supply ',nutr,food,data.supply[food][nutr])
           
    # Dec vars       
    x = LpVariable.dicts('x',data.food_items,0)
    
    # objective
    diet_lp_model += lpSum(data.objective[i] * x[i] for i in data.food_items)
    
    # constraints - loop through reqs adding an lpSum for each
    for i in data.nutrients:
        constr_LHS = lpSum(data.supply[j][i] * x[j] for j in data.food_items)
        diet_lp_model += constr_LHS >= data.reqs[i], i
            
    # upper limits
    for i in data.food_items:
        diet_lp_model += x[i] <= data.max_for_item[i], i        
            
    # the rest as before...
    # Print formulated model and optionally write it to a file
    print(diet_lp_model)
    diet_lp_model.writeLP('diet_lp_model.txt')
    
    # Solve
    result = diet_lp_model.solve(GLPK(msg=False))
    
    # Print results
    print("Status: ",LpStatus[result])
    for variable in diet_lp_model.variables():
            print(str(variable).ljust(12),' = ',value(variable))
    print(f"Objective value = {value(diet_lp_model.objective):8.2f}")     
    
    return diet_lp_model