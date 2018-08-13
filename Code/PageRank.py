import networkx as nx
def getKey(item):
    return item[1];

def find_densest_subgraph(G,n) :
    pr = nx.pagerank(G, alpha=0.9);
    pr_bis = pr.items();
    pr_bis.sort(key=getKey);
    prlist =    pr_bis [(0-n):-1] 
    return prlist;
    
