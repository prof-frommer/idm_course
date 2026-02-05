# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:34:17 2026

@author: IFrommer
"""

from amply import Amply

data = Amply("""set furniture;
             set resources;
             param prices{furniture};
             param avail{resources};  
             param required{resources,furniture};
             """)
data.load_file(open('furn.dat'))

furn_set = ['furniture1','furniture2']
assert data.furniture == furn_set
assert data.prices == dict(zip(furn_set,[120,80]))

#%%  comprehensions
x = [[u*f for u in range(1,3)] for f in [1,2,5]]
print(x)
# ans [[1, 2], [2, 4], [5, 10]]

# dict whose keys are #s from 1-7 and values are 
# True if the key is divisible by 3 and False otherwise
d = {i:i % 3 == 0 for i in range(1,8)}
print(d)
# {1: False, 2: False, 3: True, 4: False, 5: False, 6: True, 7: False}