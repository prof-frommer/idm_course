# -*- coding: utf-8 -*-
"""
Updated 1/27/23
Removed (see prior version for): addNeighbor, getWeight,
 getConnections, __str__ (more verbose)
@author: ifrommer
"""
DIRECTIONS = ('IN', 'OUT')

class Node:
    def __init__(self,location,week,supply=None,demand=None):
        self._location = location
        self._week = week
        self._supply = supply
        self._demand = demand
        self._arc_list = dict(zip(DIRECTIONS, ([],[]) ) )
        self._label = self._make_label()
                                  
    def _make_label(self):
        return '_'.join([self._location, str(self._week)])
        
    def get_location(self):
        return self._location    
    
    def get_week(self):
        return self._week
        
    def get_supply(self):
        return self._supply        

    def get_demand(self):
        return self._demand        
    
    def get_arc_list(self):
        return self._arc_list
    
    def get_pretty_arc_list(self):
        return {dir_:[alist.get_label() for alist in self._arc_list[dir_]] 
                for dir_ in self._arc_list.keys()}

    def get_label(self):
        return self._label

    def add_arc(self,arc,direction):
        if direction.upper() not in DIRECTIONS:
            raise ValueError(f'Direction must be one of {DIRECTIONS} not {direction}')
        self._arc_list[direction.upper()].append(arc)

    def __repr__(self):
        return(str(self.__dict__))