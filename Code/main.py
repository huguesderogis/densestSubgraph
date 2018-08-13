import mincut
import find_dense_avg_degr_weighted as fd_avg_deg
import graph_of_words as gow
import find_dense_kcore_weighted as fdk
import eigenvectors
import clique
import PageRank as pr
import networkx as nx
import matplotlib.pyplot as plt
import time
import nltk
import stemming as st

###### Tests on Rousseau and Vazirgiannis' paper ######

## We build the graph_of_words
#nltk.download('all')
window_size = 4;
file_txt = 'paper.txt';
stop_words = 'stopwords.txt';

dots = ["%",".",",",";","?",")","]","(","[","=","|",":","+","-","/"]   
golden_keywords = ['keyword', 'degeneracy', 'document', 'single', 'extraction', 'graph', 'representation','text', 'weighted', 'graph-of-words', 'k-core', 'decomposition'];        
golden_keywords = [x for x in golden_keywords if x not in dots]
golden_keywords = [x for x in golden_keywords if x not in stop_words]
p = st.PorterStemmer()
golden_keywords =  [p.stem(x,0,len(x)-1) for x in golden_keywords]
golden_keywords = set(golden_keywords) #remove duplicates

beg0 = time.clock()
G = gow.create_graph(file_txt,stop_words,window_size);
end0 = time.clock()
time0 = end0-beg0

print 'number of nodes of G : ', G.number_of_nodes()
print 'number of edges of G unweighted : ' , G.number_of_edges()
print 'temps de construction : ', time0

#print G
"""pos= nx.spring_layout(G)
plt.figure(1,figsize=(8,8)) 
nx.draw_networkx(G,pos)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
"""

# Using the K-Cores (weighted)
beg1 = time.clock()
S1,best_avg = fdk.find_densest_subgraph(G)
end1 = time.clock()
time1 = end1-beg1
temp = S1.nodes()
recall_Kcore = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
precision_Kcore = len(list(golden_keywords.intersection(temp)))/float(len(temp))   


# Using the avg-degr
beg2 = time.clock()
S2,best_avg2 = fd_avg_deg.find_densest_subgraph(G)
end2 = time.clock()
time2 = end2-beg2
temp = S2.nodes()
recall_AvgDeg = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
precision_AvgDeg = len(list(golden_keywords.intersection(temp)))/float(len(temp))  

#Using mincut algorithm
beg3 = time.clock()
S3, best_avg3 = mincut.find_densest_subgraph(G)
end3 = time.clock()
time3 = end3-beg3
temp = S3.nodes()
recall_Mincut = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
precision_Mincut = len(list(golden_keywords.intersection(temp)))/float(len(temp))  

#Using maximal clique 
beg5 = time.clock()
listS5, best_avg5 = clique.find_densest_subgraph(G);
end5 = time.clock()
time5 = end5-beg5
L4=[]
for x in range (0,len(listS5)):
    for y in listS5[x]:
        L4.append(y)
L4=list(set(L4))
#print L4
recall_Clique = len(list(golden_keywords.intersection(L4)))/float(len(golden_keywords))    
precision_Clique = len(list(golden_keywords.intersection(L4)))/float(len(L4))   


# PageRank
beg7 = time.clock()
list7= pr.find_densest_subgraph(G,10);
end7 = time.clock()
time7 = end7-beg7
temp = [list7[i][0] for i in range(len(list7))]
recall_PageRank = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
precision_PageRank = len(list(golden_keywords.intersection(temp)))/float(len(temp))   


#Using the function from Networkx K-Cores
beg4 = time.clock()
G.remove_edges_from(G.selfloop_edges());
S4 = nx.k_core(G);
end4 = time.clock()
time4 = end4-beg4
temp = S4.nodes()
recall_UnweightedKcore = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))    
precision_UnweightedKcore = len(list(golden_keywords.intersection(temp)))/float(len(temp))


print "\nNodes in densest subgraph using unweighted k-cores :", S4.nodes()
print 'Number of nodes : ' ,S4.number_of_nodes(),"/",G.number_of_nodes();
print 'Computation time unweighted k-cores : ' , time4;



print "\nNodes in densest subgraph using weighted k-cores :", S1.nodes()
print 'Number of nodes : ',S1.number_of_nodes(),"/",G.number_of_nodes();
print 'Avg deg : ', best_avg
print 'Computation time weighted k-cores : ' , time1;

print "\nNodes in densest subgraph using avg degree :", S2.nodes()
print 'Number of nodes : ',S2.number_of_nodes(),"/",G.number_of_nodes()
print 'Avg deg : ', best_avg2
print 'Computation time avg degree : ' , time2;

print "\nNodes in densest subgraph using mincut :", S3.nodes()
print 'Number of nodes : ',S3.number_of_nodes(),"/",G.number_of_nodes();
print 'Avg deg : ', best_avg3
print 'Computation time mincut : ' , time3;

print "\nNumber of maximal cliques :", len (listS5)
print "\nNodes in densest subgraph using cliques :"
for x in range (0,len(listS5)):
    print "\n printing clique no : ", x+1    
    print listS5[x]
print 'Number of nodes : ',len(listS5[0]),"/",G.number_of_nodes();
print 'Avg deg : ', best_avg5; #see clique.py : bestavg is the number of nodes in the clique, therefore the avg degree is bestavg-1
print 'Computation time cliques : ' , time5;

print "\nNumber of nodes chosen for pagerank :", "10","/",G.number_of_nodes()
print 'Nodes : ', list7;
print 'Computation time pagerank : ' , time7;


print "recall using K_cores : ",recall_Kcore
print "recall using average degree : ",recall_AvgDeg
print "recall using mincut : ",recall_Mincut
print "recall using k-cliques : ",recall_Clique
print "recall using pagerank : ",recall_PageRank
print "recall using unweighted K-cores : ",recall_UnweightedKcore

print "precision using K_cores : ",precision_Kcore
print "precision using average degree : ",precision_AvgDeg
print "precision using mincut : ",precision_Mincut
print "precision using k-cliques : ",precision_Clique
print "precision using pagerank : ",precision_PageRank
print "precision using unweighted K-cores : ",precision_UnweightedKcore

