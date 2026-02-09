# -*- coding: utf-8 -*-
"""
Updated 1/27/23
Removed (see prior for):  reversed
@author: IFrommer
"""
from node import Node

def check_types(test_items):
    for item in test_items:
        if type(item) != Node:
            raise ValueError(
                f'Expected node object, received {type(item)} instead')

class Arc:
    
    def __init__(self,src,dest,cost=None,capac=None,label=None):
        # src and dest are nodes
        check_types([src, dest])
        self._src = src
        self._dest = dest
        self._cost = cost
        self._capac = capac 
        self._label = label if label == None else self._make_label(label)
    
    def _make_label(self,label):
        return ','.join(['_'.join([str(part) for part in node]) 
                         for node in label])
    
    def get_src(self):
        return self._src
    
    def get_dest(self):
        return self._dest
    
    def get_cost(self):
        return self._cost
    
    def get_capac(self):
        return self._capac
    
    def get_label(self):
        return self._label

    def __str__(self):
        return f'{self._src.get_label()} -> {self._dest.get_label()}'
    