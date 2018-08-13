# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 18:11:10 2016

@author: Hugues
"""

from networkx import *

def getKey(item):
    return item[1];

def find_lowest_degree(list) :
    list.sort(key=getKey);
    return list[0];


def compute_number_of_edges (S) : 
    sum = 0
    for node in S.degree_iter() :
        deg = S.degree(node, weight='weight');    
        sum = deg.values()[0] + sum;
    return sum

def find_densest_subgraph(G):
 
    S = copy.deepcopy(G)
    
    E_init = compute_number_of_edges(S)
    N_init = S.number_of_nodes()
    avg_degree_max = (2.0*E_init)/N_init
    S_max = copy.deepcopy(S);

    while S.number_of_nodes() > 0 :

        E = compute_number_of_edges(S)
        N = S.number_of_nodes()
        avg_degree = (2.0 * E)/N
        
        if avg_degree_max <= avg_degree :
            avg_degree_max = avg_degree;
            S_max = copy.deepcopy(S);

        liste = []

        for node,deg in S.degree_iter():

            deg1 = S.degree(node, weight='weight')
            liste.append([node, deg1])
           
        nodes_min = find_lowest_degree(liste);      
        S.remove_node(nodes_min[0]);

    return S_max, avg_degree_max;

