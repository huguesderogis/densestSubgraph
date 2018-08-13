from networkx import *

def find_lowest_degree(list) :
    list.sort(key=getKey);
    return list[0];

def getKey(item):
    return item[1];

def max_core(list):
    return list[-5][1];

def list_of_nodes_in_max_core(list):
    list_of_nodes =[];
    max_cor = max_core(list);
    for x in list:
        if x[1] >= max_cor:
            list_of_nodes.append(x[0]);
    return list_of_nodes;

#Return subgraph of G with all nodes having degree >= max k-core
def find_densest_subgraph(G):
 
    S = copy.deepcopy(G)
    liste = [];
    nodes = {}
    list_core = []


    for node, deg in S.degree_iter():
        deg1 = S.degree(node, weight='weight')
        liste.append([node, deg1])
        nodes[node] = S[node]

    while len(liste)>0:
        liste.sort(key=getKey);

        node_min = liste[0][0];
        deg_min = liste[0][1];
        for node in all_neighbors(S,node_min):
            for x in liste:
                if x[0]==node and x[1]>=deg_min+S.edge[node_min][node]['weight']:
                    x[1] = x[1]-S.edge[node_min][node]['weight'];


        list_core.append(liste[0]);
        del liste[0];

    list_of_nodes_in_max=list_of_nodes_in_max_core(list_core);
    S_max = G.subgraph(list_of_nodes_in_max);
    max_cor = max_core(list_core);

    return S_max, max_cor;

