# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:10:53 2025

@author: IFrommer
"""

def df_to_dict(df):
    """ Convert dataframe to dict
    Args:
        df (pd dataframe)
    Returns:
        new_dict (dict): df indices become keys of this dict, row contents 
          become values
    """
    new_dict = dict()
    for index, row in df.iterrows():
        new_dict[index] = row.tolist()
    return new_dict

def prefs_to_ranks(prefs_dict):
    """ Convert prefs_dict to a dict of rankings, i.e. the P_i(j) of the 
         formulation
    Args:
        prefs_dict(dict): keyed by ranker, values are rank-ordered lists of
             rankees 
    Returns:
        rank_dict(dict): keyed by pair, value is 1st person's rank of 2nd person 
    """
    rank_dict = dict()
    for ranker, rankings in prefs_dict.items():
        for i in range(len(rankings)):
            rank_dict[ranker, rankings[i]] = i+1
    return rank_dict

def make_better_match_dict(prefs_dict):
    """ Pre-compute who person would have preferred to a given match
    Args:
        prefs_dict (dict): keyed by pesron, value is list of their ordered 
            partner preferences
    Returns:
        better_matches (dict): keyed by tuple of person and their match,
            value is ordered list of partners they'd have preferred to current
            match  """
    better_matches = dict()
    for person in prefs_dict:
        persons_prefs = prefs_dict[person]
        for i in range(len(persons_prefs)-1, -1, -1):
            better_matches[(person,persons_prefs[i])] = persons_prefs[0:i]
    return better_matches

def is_it_stable(matching, better_matches):
    """ Returns True if an smp matching is stable, False otherwise """
    for match in matching:
        man, woman = match
        better_women = better_matches[match]
        # loop through the better women for this man
        for w in better_women:
            better_men = better_matches[w,man]
            # if he was also a better man for her, it's a blocking pair
            if man in better_men:
                print('Blocking pair: ',match)
                return False
    return True

def get_rank_of_match(pair, prefs_dict):
    """ Return rank pair[0] gave to pair[1]
    Args:
        pair (tuple): of strings - ranker and rankee
        prefs_dict (dict):  keyed by ranker, values are rank-ordered lists of
         rankees
    Returns:
        rankees_rank (int): rank pair[0] gave pair[1]
    Example:
        for m in matched_vars:
            r = get_rank_of_match(m,prefs_dict)
            print(f'{m[0]} ranked {m[1]} {r}')
    """    
    ranker, rankee = pair
    rankers_list = prefs_dict[ranker]
    rankees_rank = rankers_list.index(rankee) + 1   # +1 due to 0-indexing
    return rankees_rank