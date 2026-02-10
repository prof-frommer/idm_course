# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:58:07 2025

@author: IFrommer
"""

import pandas as pd
from pulp import *
from smp_utils import *

mens_file = 'data/mens_prefs_1.csv'
#mens_file = 'data/Student_Preferences.csv' 
womens_file = 'data/womens_prefs_1.csv'
#womens_file = 'data/Group_Preferences.csv' 

mens_prefs = pd.read_csv(mens_file, index_col=0,header=None)
womens_prefs = pd.read_csv(womens_file, index_col=0,header=None)

women = list(womens_prefs.index)
men = list(mens_prefs.index)
pairs = [(m,w) for m in men for w in women]

all_prefs = pd.concat([mens_prefs, womens_prefs])
prefs_dict = df_to_dict(all_prefs)
better_matches = make_better_match_dict(prefs_dict)

#%%
# Create IP
smp = LpProblem('Stable_Marriage_Problem',LpMinimize)
x = # YOUR CODE HERE

# Constraints
# Each person must be matched with one other person
for # YOUR CODE HERE
    # YOUR CODE HERE

for # YOUR CODE HERE
    # YOUR CODE HERE

# Stability constraints    
for pair in pairs:
    man, woman = pair    
    better_women = better_matches[(man, woman)]
    better_men =   better_matches[(woman, man)]
        
    # Either this pair is a match
    # YOUR CODE HERE
    # or the man is with a woman he preferred to this woman
    # YOUR CODE HERE
    # or the woman is with a man she preferred to this man
    # YOUR CODE HERE
    # Constraint insures at least 1 of the above 3 conditions is true
    # YOUR CODE HERE
    
# Objective
pass

result = smp.solve(GLPK(msg=False))

#%%  Display results
matched_vars = []
print('Matches: ')
for i in men:
    for j in women:
        if value(x[i,j]) > 0:
            print(i,j,end='\t')
            matched_vars.append((i,j))
                
print("\nStatus: ",LpStatus[result])
#print("Objective value = ",value(smp.objective))

print('Stable matching? ',is_it_stable(matched_vars, better_matches))