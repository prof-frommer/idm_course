# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 08:59:07 2019
Trying to get work flow down in Python to OpenSCAD
to 3D print a polytope from an LP FR
@author: IFrommer
"""

from pulp import *
import numpy as np
from numpy.linalg import inv

# Inputs: Constraint matrix and rhs's
A0 = np.array([[3,4,2],
            [1,2,2],
            [1,1,1]])
b = np.array([[400],[300],[200]])
# Compute parameters
numVars = A0.shape[1]
m = A0.shape[0]     # # of rows of A0 = # of constraints 
assert b.shape[0] == m
totalVars = numVars + m  # totalVars includes slack variables

# Create the augmented A matrix            
idCols = np.eye(m)
A = np.hstack((A0,idCols))    

# Construct basic variable sets
bvSet = [i for i in combination(range(totalVars),m)]
# e.g. (0,1,2), ..., (0,2,5), ..., (3,4,5)


#%%
cpList2 = []    # list of dicts w/ bv set and x var values
# Loop through all possible combinations of basic vars
#  finding the corresponding corner point.
# There are |totalVars choose m| of them, listed in bvSet
for bvs in bvSet:
    # Get the columns of these BVs in original tableau
    B = A[:,bvs]    
    print('bvs are',bvs,'\nB=',B)

    # Find B inverse if it exists
    invExists = True
    try:
        Binv = inv(B)
    except Exception as err:
        print(err,'\n')
        invExists = False
        
    # If B inverse exists, find the var values (Binv*b)
    if invExists:
        print('Binv=',Binv)
        xbv = Binv.dot(b)       # the var values
        xbvT = xbv.reshape(1,numVars)  # just for printing
        del xbv    # clean-up, won't use this one        
        print('bv var values = ',xbvT)
        # If solution is basic feasible (nonneg),
        #  add it to list of cp's.
        # thin below code out given changes
        if xbvT.min() > 0:
            # this will store the values of all vars at the cp
            allVars = [0]*totalVars
            tmpDict = {}
            for i,bv in enumerate(bvs):
                allVars[bv] = xbvT[0][i]
            print('all var values = ',allVars) 
            tmpDict['BVs'] = bvs
            tmpDict['x'] = allVars[:3]
            cpList2.append(tmpDict)    
        else:   # remove later
            print('Basic solution is infeasible (neg var values)')            
        print()

#%%
# Faces - a face corresponds to a particular
#  variable equaling 0, so 1 face per variable.
# Here faces are being defined by the corner pts
#  they contain.
numFaces = totalVars
faceCPs = {i:[] for i in range(numFaces)}
faceCPs2 =  {i:[] for i in range(numFaces)}

setOfFaces = set(faceCPs.keys())
# Loop through CPs, finding which faces each is on
for i,cp in enumerate(cpList2):
    bvs = cp['BVs']
    labl = ''.join([str(k) for k in bvs])
    print('BVs=',bvs,' ',labl)
    facesItsOn = setOfFaces.difference(set(bvs))
    print('Faces it is on=',facesItsOn)
    for face in facesItsOn:
        faceCPs[face].append(labl)
        faceCPs2[face].append(i)
# Delete any empty faces
fv = list(faceCPs.values())
empties = [i for i in range(len(fv)) if fv[i] ==[]]
empties.reverse()
for empty in empties:
    faceCPs.pop(empty)      
    faceCPs2.pop(empty)
# I think it's working, but double-check
#  and go through once more to clean up

print(10*'- ','\n')
print('corner point list = ')
pprint.pprint(cpList2)
print('\nfaces-cps table:')
pprint.pprint(faceCPs)

#%%
ptListForSolid = [d['x'] for d in cpList2]
facesForSolid = list(faceCPs2.values())

#%%
from solid import *
p = polyhedron(ptListForSolid,facesForSolid)
print(scad_render(p))