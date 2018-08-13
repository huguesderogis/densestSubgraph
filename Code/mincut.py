from networkx import *


def compute_number_of_edges (S) : 
    sum = 0
    for node in S.degree_iter() :
        deg = S.degree(node, weight='weight');
        #print deg.values()        
        sum = deg.values()[0] + sum;
    return sum

def find_densest_subgraph(G):

	E=compute_number_of_edges(G);
	N=G.number_of_nodes();

	mind = 0;
	maxd = N;
	Vs = [];
	threshold = 1.0/ (N * (N-1));
	cut_value_max=0;


	while (maxd - mind )> threshold :
		
		g = (maxd + mind)/2.0
		
		liste_nodes = G.nodes(data = False)
		source = 'source'
		sink = 'sink'
		
		DG = nx.DiGraph()
		DG.add_node(source)
		DG.add_node(sink)
		for u,v in G.edges():
			DG.add_edge(u,v, capacity = G.edge[u][v]['weight']);
			DG.add_edge(v,u,capacity=G.edge[u][v]['weight']);
		for x in G.nodes():
			if x != source and x!=sink:
				DG.add_edge(source,x, capacity=E);
		for x in G.nodes():
			if x != source and x!= sink :
				deg = G.degree(x, weight='weight')
				DG.add_edge(x,sink, capacity=E+2*g-deg);
		cut_value, partition = nx.minimum_cut(DG,source,sink, capacity='capacity');

		if (len(partition[0]) == 1 ) and (partition[0].pop()==source ):
			maxd = g;
			
		else :
			mind = g;
			
			Vs = [x for x in partition[0] if x != source ]
			cut_value_max=cut_value;
	length_Vs = len(Vs);	

	V_subgraph = G.subgraph(Vs)
	avg_degree_max = 2.0*compute_number_of_edges(V_subgraph)/V_subgraph.number_of_nodes();
	
	return V_subgraph, avg_degree_max;

