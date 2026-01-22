# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 12:54:24 2026 @author: IFrommer
Optimal
Objective value 540.0
x1 = 600.0
x2 = 240.0
x3 = 160.0
"""

from pulp import *

coffee_lp = LpProblem('Coffee_LP')

x1 = LpVariable('x1',lowBound=0)
x2 = LpVariable('x2',lowBound=0)
x3 = LpVariable('x3',lowBound=0)

coffee_lp += .5*x1 + .7*x2 + .45*x3, 'cost ($)'

coffee_lp += x1 + x2 + x3 >= 1000, 'lbs of product'
coffee_lp += 10*x2 - 15*x3 >= 0, 'aroma'
coffee_lp += 6*x1 - 8*x2 - 5*x3 >= 0, 'taste'
coffee_lp += x1 <= 600
#coffee_lp += x2 <= 600
#coffee_lp += x3 <= 400

result = coffee_lp.solve(PULP_CBC_CMD(msg=False))
print(LpStatus[result])
print('Objective value',value(coffee_lp.objective))
for var in coffee_lp.variables():
    print(var,'=',value(var))
