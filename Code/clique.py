import networkx as nx
#tests
"""
import matplotlib.pyplot as plt
S = nx.Graph()
S.add_node('numer')
S.add_node('kind')
S.add_node('system')
S.add_node('-matric')
S.add_edge('system','numer')
S.add_edge('-matric','numer')
S.add_edge('-matric','kind')
S.add_edge('-matric','system')

#pos= nx.spring_layout(S)
#plt.figure(1,figsize=(5,5)) 
#nx.draw_networkx(S,pos)

from networkx.algorithms.approximation import clique
print clique.max_clique(S)  #-> doesn't work

l= list(nx.find_cliques(S))
print l
Max = max(len(clique) for clique in l)
print Max
cliques=[clique for clique in l if len(clique)==Max] 
print cliques #-> OK
"""
def compute_number_of_edges (S) : 
    sum = 0
    for node in S.degree_iter() :
        deg = S.degree(node, weight='weight');
        #print deg.values()        
        sum = deg.values()[0] + sum;
    return sum

def find_densest_subgraph(G) :
    Slist=list(nx.find_cliques(G))
    avg_best = max(len(clique) for clique in Slist)
    cliques=[clique for clique in Slist if len(clique)==avg_best]

    avg_deg = 0;
    for clique in cliques:
        clique_subgraph = G.subgraph(clique)
        N = clique_subgraph.number_of_nodes()
        E = compute_number_of_edges(clique_subgraph)

        avg_deg = 0.5*(avg_deg+(2.0*E)/N)

    return cliques, avg_deg