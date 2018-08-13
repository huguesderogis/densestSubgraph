import os.path
import glob
import time
import networkx as nx
import stemming as st
import mincut
import find_dense_avg_degr_weighted as fd_avg_deg
import graph_of_words as gow
import find_dense_kcore_weighted as fdk
#import eigenvectors
import clique
import PageRank as pr
import nltk
#import matplotlib.pyplot as plt

##################################################################################
#                                                                                #
# File hulth2003.py : generate results from Database Hulth2003 : 500 papers      #
#                                                                                #
##################################################################################


path = "Hulth2003/Test"
os.chdir(path)

L=glob.glob("*.abstr")
K=glob.glob("*.uncontr")
stop_words = 'stopwords.txt'
window_size = 4;
print "nombre de tests : ",len(L)

time_init = 0
time_Kcore = 0
time_AvgDeg = 0
time_Mincut = 0
time_Clique = 0
time_PageRank = 0
time_UnweightedKcore = 0

recall_Kcore = 0
recall_AvgDeg = 0
recall_Mincut = 0
recall_Clique = 0
recall_PageRank = 0
recall_UnweightedKcore = 0

precision_Kcore = 0
precision_AvgDeg = 0
precision_Mincut = 0
precision_Clique = 0
precision_PageRank = 0
precision_UnweightedKcore = 0
for i in xrange(len((L))):#xrange(len(L)):#): #len(l)=50
    print 'running... ', 100.*i/(len(L)), '%'
    file_txt = L[i]    
    dots = ["%",".",",",";","?",")","]","(","[","=","|",":","+","-","/"]      
    file_golden = open(K[i], 'r')
    s= file_golden.read()
    golden_keywords=nltk.word_tokenize(s)        
    golden_keywords = [x for x in golden_keywords if x not in dots]
    p = st.PorterStemmer()
    golden_keywords =  [p.stem(x,0,len(x)-1) for x in golden_keywords]
    golden_keywords = set(golden_keywords) #remove duplicates
    
    #constructiong GoW    
    beg0 = time.clock()
    G = gow.create_graph(file_txt,stop_words,window_size);
    end0 = time.clock()
    time0 = end0-beg0
    time_init += time0
    
    # Using the K-Cores
    beg1 = time.clock()
    S1,best_avg = fdk.find_densest_subgraph(G)
    end1 = time.clock()
    time1 = end1-beg1
    time_Kcore += time1
    temp = S1.nodes()
    recall1 = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
    recall_Kcore += recall1/(len(L))
    precision1 = len(list(golden_keywords.intersection(temp)))/float(len(temp))   
    precision_Kcore += precision1/len(L) 
    
    # Using the avg-degr
    beg2 = time.clock()
    S2,best_avg2 = fd_avg_deg.find_densest_subgraph(G)
    end2 = time.clock()
    time2 = end2-beg2
    time_AvgDeg += time2
    temp = S2.nodes()
    recall2 = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
    recall_AvgDeg += recall2/len(L) 
    precision2 = len(list(golden_keywords.intersection(temp)))/float(len(temp))   
    precision_AvgDeg += precision2/len(L) 
    
    #Using mincut algorithm
    beg3 = time.clock()
    S3, best_avg3 = mincut.find_densest_subgraph(G)
    end3 = time.clock()
    time3 = end3-beg3
    time_Mincut += time3
    temp = S3.nodes()
    recall3 = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
    recall_Mincut += recall3/len(L) 
    precision3 = len(list(golden_keywords.intersection(temp)))/float(len(temp))   
    precision_Mincut += precision3/len(L) 
    
    #Using maximal clique 
    beg4 = time.clock()
    listS4, best_avg4 = clique.find_densest_subgraph(G);
    end4 = time.clock()
    time4 = end4-beg4
    time_Clique += time4
    L4=[]
    for x in range (0,len(listS4)):
        for y in listS4[x]:
            L4.append(y)
    L4=list(set(L4))
    #print L4
    recall4 = len(list(golden_keywords.intersection(L4)))/float(len(golden_keywords))   
    recall_Clique += recall4/len(L) 
    precision4 = len(list(golden_keywords.intersection(L4)))/float(len(L4))   
    precision_Clique += precision4/len(L) 
    # PageRank
    beg5 = time.clock()
    list5= pr.find_densest_subgraph(G,10);
    end5= time.clock()
    time5 = end5-beg5
    time_PageRank += time5 
    temp = list5
    recall5 = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
    recall_PageRank += recall5/len(L) 
    precision5 = len(list(golden_keywords.intersection(temp)))/float(len(temp))   
    precision_PageRank += precision5/len(L) 

    #Using the function from Networkx K-Cores
    beg6 = time.clock()
    G.remove_edges_from(G.selfloop_edges());
    S6 = nx.k_core(G);
    temp = S6.nodes()
    end6 = time.clock()
    time6 = end6-beg6
    time_UnweightedKcore += time6
    recall6 = len(list(golden_keywords.intersection(temp)))/float(len(golden_keywords))   
    recall_UnweightedKcore += recall6/len(L) 
    precision6 = len(list(golden_keywords.intersection(temp)))/float(len(temp))   
    precision_UnweightedKcore += precision6/len(L) 

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

print "time using K_cores : ",time_Kcore
print "time using average degree : ",time_AvgDeg
print "time using mincut : ",time_Mincut
print "time using k-cliques : ",time_Clique
print "time using pagerank : ",time_PageRank
print "time using unweighted K-cores : ",time_UnweightedKcore
    