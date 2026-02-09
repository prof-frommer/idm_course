"""  
v3 - refactoring in 2023
V2 - minor edits in Part III (added comments)
Based on 2020 update of transshipment code using AMPLY and Arc & Node objects
some notes:
To make things a little simpler:    
- procurement costs rolled up with the transport costs
- added capability to add week 7 demand nodes to balance problem if
 supply exceeds demand. Demand > Supply functionality not built yet.
"""
#%% PART I - load problem data into variables

from pulp import *
from amply import *
from arc import Arc
from node import Node

def load_data(dat_file):
    data = Amply("""
                 set locations;
                 set weeks;
                 set arc_capac;
                 set arc_costs;
                 set arc_times;
                 param supply{locations,weeks};
                 param demand{locations,weeks};
                 param inv_capac{locations};
                 param inv_cost{locations};
                 """)
    data.load_file(open(DAT_FILE))   
    return data

def extract_arc_info(data):
    arc_capac = data.arc_capac[0]  
    # Rows are stored in dat file like (src,dest,cost or time)
    # Convert to dict { (src,dest): cost or time, ...}
    arc_costs  = {row[:2]:row[2] for row in data.arc_costs.data}
    lead_times = {row[:2]:row[2] for row in data.arc_times.data}
    return arc_capac, arc_costs, lead_times 

def extract_node_names(data):
    node_names = dict()
    nodes_with_demand = set(data.demand.data.keys())
    nodes_with_supply = set(data.supply.data.keys())
    node_names['demand'] = nodes_with_demand.difference(nodes_with_supply)
    node_names['supply'] = nodes_with_supply.difference(nodes_with_demand)
    node_names['distr'] = set(data.locations).difference(
                            node_names['demand'].union(node_names['supply']))
    return node_names

def compute_sup_dem(data, node_names):
    total_supply = 0;        total_demand = 0
    for s in node_names['supply']:
        total_supply += sum(data.supply.data[s].values())
    for d in node_names['demand']:
        total_demand += sum(data.demand.data[d].values())
    return total_supply, total_demand

def compute_dummy_demand(total_supply, total_demand):
    total_dummy_demand = 0    
    if total_supply > total_demand:
        total_dummy_demand = total_supply - total_demand 
    elif total_supply < total_demand:
        msg = 'Demand exceeds supply. Functionality not yet built. Exiting.'
        raise ValueError(msg)
    return total_dummy_demand

def obtain_sup_dem_info(data, node_names):
    supply_wks = list(list(data.supply.data.values())[0].keys())
    demand_wks = list(list(data.demand.data.values())[0].keys())
    max_dem_wk = max(demand_wks)
    total_supply, total_demand = compute_sup_dem(data, node_names)
    total_dummy_demand = compute_dummy_demand(total_supply, total_demand)
    return supply_wks, demand_wks, max_dem_wk, total_supply, total_demand, \
        total_dummy_demand

DAT_FILE = 'data/mptp_data_quiz2026.dat'

data = load_data(DAT_FILE)
arc_capac, arc_costs, lead_times = extract_arc_info(data)
node_names = extract_node_names(data)
supply_wks, demand_wks, max_dem_wk, total_supply, total_demand, \
    total_dummy_demand = obtain_sup_dem_info(data, node_names)

#%% PART II - Create pathways
# Compute paths of arcs from sup to dem, ruling out
#  ones that arrive after max demand week

def add_nodes_and_arcs(supply_node, distr_node, demand_node,
                       wk_A, wk_B, wk_C):
    # add path's nodes to the node list
    n1 = (supply_node, int(wk_A));     path_node_labels = {n1}
    n2 = (distr_node, int(wk_B));      path_node_labels.add(n2)
    n3 = (demand_node, int(wk_C));     path_node_labels.add(n3)
    # add path's arcs to the arc list
    a1 = (n1, n2);    path_arc_labels = {a1}
    a2 = (n2, n3);    path_arc_labels.add(a2)
    return path_node_labels, path_arc_labels

def compute_paths(node_names, supply_wks, lead_times, max_dem_wk):
    path_node_labels = set(); path_arc_labels = set()
    for supply_node in node_names['supply']:
        for wk_A in supply_wks:
            for distr_node in node_names['distr']:
                wk_B = wk_A + lead_times[(supply_node, distr_node)]
                for demand_node in node_names['demand']:
                    wk_C = wk_B + lead_times[(distr_node, demand_node)]
                    if wk_C <= max_dem_wk: # viable path
                        new_node_labels, new_arc_labels = \
                            add_nodes_and_arcs(supply_node, distr_node, 
                                             demand_node, wk_A, wk_B, wk_C)
                        path_node_labels = path_node_labels.union(new_node_labels)
                        path_arc_labels =  path_arc_labels.union(new_arc_labels)
    return path_node_labels, path_arc_labels
   
path_node_labels, path_arc_labels = compute_paths(node_names, supply_wks, 
                                        lead_times, max_dem_wk)              

#%% PART III - Create node objects, inventory arcs and dummy demand nodes
# Make the LP node objects.  Store them in a dictionary keyed by loc,wk tuple

def make_lp_node_objects(data, path_node_labels):
    node_objects = dict() 
    for node_label in path_node_labels:
        locn, wk = node_label
        if locn in node_names['supply']:
            supply_amt = data.supply.data[locn][wk]
        else:
            supply_amt = None
        if locn in node_names['demand']:
            demand_amt = data.demand.data[locn][wk]   
        else:
            demand_amt = None
        node_objects[node_label] = Node(locn, wk, supply_amt,demand_amt)
    return node_objects

def make_inv_arc_and_dummy_nodes(data, node_objects, path_arc_labels):
     # Make the inventory arcs and dummy demand nodes if necessary
    inv_locs = list(data.inv_cost.data.keys())  # inventory nodes
    for locn in inv_locs:
        # Get all node labels corresponding to this node.
        inv_node_labels = [k for k in node_objects.keys() if k[0]==locn]
        # Get a list of all weeks for this node.
        week_vals = sorted([i[1] for i in inv_node_labels])
        # Add arc labels for the new inventory arcs
        for w in week_vals:   # this goes out an extra week
            path_arc_labels.add(   ( (locn,w), (locn,w+1) )    )
        # add dummy demand nodes if necessary (in the last week)
        if total_dummy_demand:
            dummy_demand_per_node = total_dummy_demand / len(node_names['demand'])
            node_objects[(locn,w+1)] = Node(locn,w+1,demand =dummy_demand_per_node)
    return node_objects, path_arc_labels

node_objects = make_lp_node_objects(data, path_node_labels)
node_objects, path_arc_labels = make_inv_arc_and_dummy_nodes(data, 
                                            node_objects, path_arc_labels)


#%% PART IV  -  CREATE LP ARC OBJECTS    
# Create the LP arcs objects from the paths.

def make_lp_arc_objects(data, path_arc_labels, node_objects):
    arc_objects = dict()
    for arc_label in path_arc_labels:   # e.g. an arcLabel looks like:('CHI',1),('HOU',3)
        src_label, dest_label = arc_label
        src_loc, dest_loc = src_label[0], dest_label[0]
    
        # build cost and capacity - 2 types (rolled procurmnt into transport in dat)
        if src_loc == dest_loc:  # it's an inventory arc 
            cost = data.inv_cost[src_loc]
            capac = data.inv_capac[src_loc]
        else:   # it's a standard transportation arc
            cost = arc_costs[(src_loc, dest_loc)]
            capac = arc_capac
    
        # Make arc object. Its src, dest vars are node object refs.        
        arc_object = Arc(node_objects[src_label],node_objects[dest_label], cost, 
                         capac, arc_label)     
        arc_objects[arc_object.get_label()] = arc_object
        # Update those nodes joined by this arc
        node_objects[src_label].add_arc(arc_object, 'out')
        node_objects[dest_label].add_arc(arc_object, 'in')
    return arc_objects, node_objects

arc_objects, node_objects = make_lp_arc_objects(data, 
                                    path_arc_labels, node_objects)
#%% PART V - CREATE THE LP
# Instantiate LP model object
mptp_lp = LpProblem('MultiperiodTransshipmentLP',sense=LpMinimize)

# Define variables
x = LpVariable.dicts("x", arc_objects, lowBound=0)

# Objective
mptp_lp += lpSum(arc_objects[arc].get_cost() * x[arc] for arc in arc_objects)

# Constraints
for arc in arc_objects:        #  Arc capacity
    mptp_lp += x[arc] <= arc_objects[arc].get_capac() #, arc

# Flow balance
for node_object in node_objects.values():
    supply = node_object.get_supply()
    
    arcs_in = node_object.get_arc_list()['IN']
    flow_in = lpSum(x[arc.get_label()] for arc in arcs_in)
    
    arcs_out = node_object.get_arc_list()['OUT']
    flow_out = lpSum(x[arc.get_label()] for arc in arcs_out)
    
    demand = node_object.get_demand()
    #print(supply,flow_in,flow_out,demand)
    mptp_lp += supply + flow_in - flow_out - demand == 0, node_object.get_label()

#%% PART VI - Solve, display results    
res = mptp_lp.solve(PULP_CBC_CMD(msg=False))

import sys
out_file = 'mptp_solution.txt'
file_obj = open(out_file,'w')     
for output in [file_obj, sys.stdout]:
    print(mptp_lp, file = output)
    print('\nSolution\nVariable Values:',file=output)
    for var in mptp_lp.variables():
        if value(var) > 0:
            print(str(var),value(var),file=output)
    print("Status: ",LpStatus[res],file=output)
    print("Objective value = ",value(mptp_lp.objective),file=output)
file_obj.close()